import datetime
from decimal import Decimal

import mock
import pytest
import pytz

from django.http.response import Http404
from django_dynamic_fixture import G

from appointment.models import Appointment, AppointmentService
from appointment.preview import (
    AppointmentPreviewRequest,
    AppointmentPreviewResponse,
    AppointmentServicePreview,
    build_appointment_preview_dict,
)
from appointment.types import AppointmentStatus
from client.models import Client
from core.utils import calculate_card_fee, calculate_tax
from pricing import CalculatedPrice, DiscountType
from salon.models import Stylist, StylistService


class TestBuildAppointmentPreviewDict(object):

    @pytest.mark.django_db
    def test_bad_appointment_uuid(self):
        stylist = G(Stylist)
        appointment = G(
            Appointment, datetime_start_at=datetime.datetime(2018, 1, 1, 0, 0, tzinfo=pytz.UTC)
        )
        preview_request = AppointmentPreviewRequest(
            services=[],
            datetime_start_at=datetime.datetime(2018, 1, 1, 0, 0, tzinfo=pytz.UTC),
            has_tax_included=False,
            has_card_fee_included=False,
            appointment_uuid=appointment.uuid
        )
        with pytest.raises(Http404):
            build_appointment_preview_dict(
                stylist=stylist,
                client=None,
                preview_request=preview_request
            )

    @pytest.mark.django_db
    def test_without_services(self):
        stylist: Stylist = G(Stylist)
        preview_request = AppointmentPreviewRequest(
            services=[],
            datetime_start_at=datetime.datetime(2018, 1, 1, 0, 0, tzinfo=pytz.UTC),
            has_tax_included=False,
            has_card_fee_included=False,
        )
        preview_dict = build_appointment_preview_dict(
            stylist=stylist,
            client=None,
            preview_request=preview_request
        )
        assert(preview_dict.conflicts_with.count() == 0)
        # we can't compare QuerySets, so will just replace the field
        preview_dict = preview_dict._replace(conflicts_with=None)
        assert(preview_dict == AppointmentPreviewResponse(
            grand_total=0,
            total_client_price_before_tax=0,
            total_tax=0,
            total_card_fee=0,
            duration=stylist.service_time_gap,
            conflicts_with=None,
            has_tax_included=False,
            has_card_fee_included=False,
            services=[],
            stylist=stylist,
            datetime_start_at=datetime.datetime(2018, 1, 1, 0, 0, tzinfo=pytz.UTC),
            status=AppointmentStatus.NEW,
            total_discount_percentage=0,
            total_discount_amount=0,
            tax_percentage=float(stylist.tax_rate) * 100,
            card_fee_percentage=float(stylist.card_fee) * 100,
        ))

    @pytest.mark.django_db
    @mock.patch(
        'appointment.preview.calculate_price_and_discount_for_client_on_date',
        lambda service, client, date: CalculatedPrice.build(
            19, DiscountType.WEEKDAY, 5
        )
    )
    def test_without_existing_appointment_with_new_services(self):
        stylist: Stylist = G(Stylist)
        service: StylistService = G(StylistService, stylist=stylist, regular_price=20)
        preview_request = AppointmentPreviewRequest(
            services=[
                {'service_uuid': service.uuid}
            ],
            datetime_start_at=datetime.datetime(2018, 1, 1, 0, 0, tzinfo=pytz.UTC),
            has_tax_included=False,
            has_card_fee_included=False,
        )
        preview_dict = build_appointment_preview_dict(
            stylist=stylist,
            client=None,
            preview_request=preview_request
        )
        assert (preview_dict.conflicts_with.count() == 0)
        # we can't compare QuerySets, so will just replace the field
        preview_dict = preview_dict._replace(conflicts_with=None)
        assert (preview_dict == AppointmentPreviewResponse(
            grand_total=19,
            total_client_price_before_tax=19,
            total_tax=calculate_tax(Decimal(19), stylist.tax_rate),
            total_card_fee=calculate_card_fee(Decimal(19), stylist.card_fee),
            duration=stylist.service_time_gap,
            conflicts_with=None,
            has_tax_included=False,
            has_card_fee_included=False,
            services=[
                AppointmentServicePreview(
                    service_name=service.name,
                    service_uuid=service.uuid,
                    client_price=19,
                    regular_price=service.regular_price,
                    duration=service.duration,
                    is_original=True,
                    uuid=None,
                ),
            ],
            stylist=stylist,
            datetime_start_at=datetime.datetime(2018, 1, 1, 0, 0, tzinfo=pytz.UTC),
            status=AppointmentStatus.NEW,
            total_discount_percentage=5,
            total_discount_amount=1,
            tax_percentage=float(stylist.tax_rate) * 100,
            card_fee_percentage=float(stylist.card_fee) * 100,
        ))

    @pytest.mark.django_db
    def test_with_existing_appointment_with_new_services(self):
        stylist: Stylist = G(Stylist)
        existing_service: StylistService = G(
            StylistService, stylist=stylist, regular_price=20,
        )
        service: StylistService = G(
            StylistService, stylist=stylist, regular_price=50
        )
        service2: StylistService = G(
            StylistService, stylist=stylist, regular_price=50
        )
        appointment: Appointment = G(
            Appointment, stylist=stylist,
            datetime_start_at=datetime.datetime(2018, 1, 1, 0, 0, tzinfo=pytz.UTC),
            total_discount_percentage=50, discount_type=DiscountType.WEEKDAY
        )
        appointment_service: AppointmentService = G(
            AppointmentService,
            appointment=appointment,
            service_uuid=existing_service.uuid,
            is_original=True,
            service_name=existing_service.name,
            regular_price=20,
            calculated_price=10,
            client_price=10,
            applied_discount=DiscountType.WEEKDAY,
            discount_percentage=50
        )
        preview_request = AppointmentPreviewRequest(
            services=[
                {'service_uuid': service.uuid},
                {'service_uuid': service2.uuid, 'client_price': 5},
                {'service_uuid': existing_service.uuid},
            ],
            datetime_start_at=datetime.datetime(2018, 1, 1, 0, 0, tzinfo=pytz.UTC),
            has_tax_included=False,
            has_card_fee_included=False,
            appointment_uuid=appointment.uuid
        )
        preview_dict = build_appointment_preview_dict(
            stylist=stylist,
            client=None,
            preview_request=preview_request
        )
        assert (preview_dict.conflicts_with.count() == 0)
        # we can't compare QuerySets, so will just replace the field
        preview_dict = preview_dict._replace(conflicts_with=None)
        assert (preview_dict == AppointmentPreviewResponse(
            grand_total=38,
            total_client_price_before_tax=38,
            total_tax=calculate_tax(Decimal(38), tax_rate=stylist.tax_rate),
            total_card_fee=calculate_card_fee(Decimal(38), card_fee=stylist.card_fee),
            duration=stylist.service_time_gap,
            conflicts_with=None,
            has_tax_included=False,
            has_card_fee_included=False,
            services=[
                AppointmentServicePreview(
                    service_name=service.name,
                    service_uuid=service.uuid,
                    client_price=25,
                    regular_price=50,
                    duration=service.duration,
                    is_original=False,
                    uuid=None,
                ),
                AppointmentServicePreview(
                    service_name=service2.name,
                    service_uuid=service2.uuid,
                    client_price=3,  # 50% discount should have been applied + round_half_up to $3
                    regular_price=50,
                    duration=service.duration,
                    is_original=False,
                    uuid=None,
                ),
                AppointmentServicePreview(
                    service_name=existing_service.name,
                    service_uuid=existing_service.uuid,
                    client_price=10,
                    regular_price=20,
                    duration=existing_service.duration,
                    is_original=True,
                    uuid=appointment_service.uuid,
                ),
            ],
            stylist=stylist,
            datetime_start_at=datetime.datetime(2018, 1, 1, 0, 0, tzinfo=pytz.UTC),
            status=appointment.status,
            total_discount_percentage=50,
            total_discount_amount=82,
            tax_percentage=float(stylist.tax_rate) * 100,
            card_fee_percentage=float(stylist.card_fee) * 100,
        ))

    @pytest.mark.django_db
    @mock.patch(
        'appointment.preview.calculate_price_and_discount_for_client_on_date',
        lambda service, client, date: CalculatedPrice.build(
            19, DiscountType.WEEKDAY, 5
        )
    )
    def test_with_existing_client(self):
        stylist: Stylist = G(Stylist)
        service: StylistService = G(StylistService, stylist=stylist, regular_price=20)
        client: Client = G(Client)
        preview_request = AppointmentPreviewRequest(
            services=[
                {'service_uuid': service.uuid}
            ],
            datetime_start_at=datetime.datetime(2018, 1, 1, 0, 0, tzinfo=pytz.UTC),
            has_tax_included=False,
            has_card_fee_included=False,
        )
        preview_dict = build_appointment_preview_dict(
            stylist=stylist,
            client=client,
            preview_request=preview_request
        )
        assert (preview_dict.conflicts_with.count() == 0)
        # we can't compare QuerySets, so will just replace the field
        preview_dict = preview_dict._replace(conflicts_with=None)
        assert (preview_dict == AppointmentPreviewResponse(
            grand_total=19,
            total_client_price_before_tax=19,
            total_tax=calculate_tax(Decimal(19), tax_rate=stylist.tax_rate),
            total_card_fee=calculate_card_fee(Decimal(19), card_fee=stylist.card_fee),
            duration=stylist.service_time_gap,
            conflicts_with=None,
            has_tax_included=False,
            has_card_fee_included=False,
            total_discount_percentage=5,
            total_discount_amount=1,
            services=[
                AppointmentServicePreview(
                    service_name=service.name,
                    service_uuid=service.uuid,
                    client_price=19,
                    regular_price=service.regular_price,
                    duration=service.duration,
                    is_original=True,
                    uuid=None,
                ),
            ],
            stylist=stylist,
            datetime_start_at=datetime.datetime(2018, 1, 1, 0, 0, tzinfo=pytz.UTC),
            status=AppointmentStatus.NEW,
            tax_percentage=float(stylist.tax_rate) * 100,
            card_fee_percentage=float(stylist.card_fee) * 100,

        ))
