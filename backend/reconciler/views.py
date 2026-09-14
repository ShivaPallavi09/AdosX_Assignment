from django.http import JsonResponse
from rest_framework.views import APIView
from reconciler.models import SystemARecord, SystemBRecord, Location
from reconciler.services.comparator import reconcile_records

class DiscrepancyListView(APIView):
    def get(self, request):
        tenant_org = request.query_params.get("org_id")
        reason_filter = request.query_params.get("reason")

        if not tenant_org:
            return JsonResponse({"error": "org_id query parameter is required"}, status=400)

        records_a = list(SystemARecord.objects.values("record_id", "value", "location_id"))
        records_b = list(SystemBRecord.objects.values("record_ref", "value", "location_id"))
        
        locations = Location.objects.all()
        location_map = {loc.location_id: loc.org_id for loc in locations}

        all_discrepancies = reconcile_records(records_a, records_b, location_map)

        tenant_data = [d for d in all_discrepancies if d.org_id == tenant_org]

        if reason_filter and reason_filter != "ALL":
            tenant_data = [d for d in tenant_data if d.reason == reason_filter]

        return JsonResponse({"results": [d.__dict__ for d in tenant_data]}, safe=False)