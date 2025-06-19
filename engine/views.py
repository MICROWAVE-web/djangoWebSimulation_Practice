from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse

from .serializers import CellSerializer
from .simulation_engine.simulation import simulation_instance
from .simulation_engine import cell


class CellListView(APIView):
    def get(self, request):
        serializer = CellSerializer(simulation_instance.cells, many=True)
        return Response(serializer.data)


class StepSimulationView(APIView):
    def get(self, request):
        simulation_instance.update()
        return Response({"status": "step completed"})


class ResetSimulationView(APIView):
    def get(self, request):
        simulation_instance.reset()
        serializer = CellSerializer(simulation_instance.cells, many=True)
        return Response(serializer.data)


def change_value(request, param, val):
    setattr(cell, param.upper(), val)
    return JsonResponse({"status": "ok"})


def get_param(request, param):
    val = getattr(cell, param.upper())
    return JsonResponse({"status": "ok", "value": val})
