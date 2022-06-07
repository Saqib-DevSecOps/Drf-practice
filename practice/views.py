from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from rest_framework import status, viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from practice.models import Student
from practice.serializers import StudentSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
import io
from rest_framework.generics import GenericAPIView, ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, \
    ListCreateAPIView, RetrieveUpdateDestroyAPIView, DestroyAPIView
from rest_framework.mixins import ListModelMixin, DestroyModelMixin, RetrieveModelMixin, CreateModelMixin, \
    UpdateModelMixin
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny, DjangoModelPermissions, \
    DjangoModelPermissionsOrAnonReadOnly, IsAdminUser
from rest_framework.authentication import BasicAuthentication, TokenAuthentication, SessionAuthentication, \
    BaseAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
def students(request):
    stu = Student.objects.all()
    serializer = StudentSerializer(stu, many=True)
    json_data = JSONRenderer().render(serializer.data)
    return HttpResponse(json_data, content_type='application/json')


def detail(request, pk):
    student = Student.objects.get(id=pk)
    serializer = StudentSerializer(student)
    json_data = JSONRenderer().render(serializer.data)
    return HttpResponse(json_data, content_type='application/json')


def delete(request, pk):
    student = Student.objects.get(id=pk)
    student.delete()
    return HttpResponse(status=status.HTTP_200_OK)


def Create(request):
    json_data = request.data
    stream = io.BytesIO(json_data)
    python_data = JSONParser().parse(stream)
    serializer = StudentSerializer(python_data)
    if serializer.is_valid():
        serializer.save()
        data = {'msg': 'successfully created'}
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, status=status.HTTP_201_CREATED)


def update(request, pk):
    stu = Student.objects.get(id=pk)
    json_data = request.data
    stream = io.BytesIO(json_data)
    python_data = JSONParser().parse(stream)
    serializer = StudentSerializer(stu, python_data)
    if serializer.is_valid():
        serializer.save()
        data = {'msg': 'successfully created'}
        json_data = JSONRenderer().render(data)
        return HttpResponse(json_data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def studentapi(request, pk=None):
    if request.method == 'GET':
        id = pk
        if id is not None:
            stu = Student.objects.get(id=pk)
            serializer = StudentSerializer(stu)
            return Response(serializer.data)
        student = Student.objects.all()
        stu = StudentSerializer(student, many=True)
        return Response(stu.data)

    if request.method == 'POST':
        data = request.data
        stu = StudentSerializer(data=data)
        if stu.is_valid():
            stu.save()
            return Response({'msg': 'created'})
        return Response(stu.errors)

    if request.method == 'PUT':
        id = pk
        student = Student.objects.get(id=id)
        stu = StudentSerializer(student, data=request.data)
        if stu.is_valid():
            stu.save()
            return Response({'msg': 'created'})
        return Response(stu.errors)

    if request.method == 'PATCH':
        id = pk
        student = Student.objects.get(id=id)
        stu = StudentSerializer(student, data=request.data, partial=True)
        if stu.is_valid():
            stu.save()
            return Response({'msg': 'created'})
        return Response(stu.errors)

    if request.method == 'DELETE':
        id = pk
        student = Student.objects.get(id=id)
        student.delete()
        return Response({'msg': 'Deleted'})


@csrf_exempt
def studentcreate(request):
    if request.method == 'POST':
        json_data = request.data
        stream = io.BytesIO(json_data)
        data = JSONParser().parse(stream)
        serializer = StudentSerializer(data)
        if serializer.is_valid():
            serializer.save()
            res = {'msg': 'Data Created'}
            json_data = JSONRenderer().render(res)
            return HttpResponse(data=json_data, content_type='application/json')


def studentlistview(request):
    if request.method == "POST":
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        id = python_data.get('id', None)
        if id is not None:
            student = Student.object.get(id=id)
            stu = StudentSerializer(student)
            json_data = JSONRenderer().render(stu)
            return HttpResponse(json_data, content_type='application/json')
    student = Student.objects.all()
    stu = StudentSerializer(student, many=True)
    json_data = JSONRenderer().render(stu.data)
    return HttpResponse(json_data, content_type='application/json')


class StudentApi(APIView):
    def get(self, request, pk=None):
        id = pk
        if id is not None:
            student = Student.objects.get(id=pk)
            student = StudentSerializer(student)
            return Response(student.data)
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None, format=None):
        student = Student.objects.get(id=pk)
        serializer = StudentSerializer(student, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Succesfully Update'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None, format=None):
        student = Student.objects.get(id=pk)
        serializer = StudentSerializer(student, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Succesfully Update'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        student = Student.objects.get(id=pk)
        student.delete()
        return Response({'Msg': 'Successfully Deleted'}, status=status.HTTP_400_BAD_REQUEST)


# Generic View

class StudentList(GenericAPIView, ListModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get(self, request, *args, **kwargs):
        return self.list(self, request, *args, **kwargs)


class StudentDetail(GenericAPIView, RetrieveModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def retrieve(self, request, *args, **kwargs):
        return self.get(self, request, *args, **kwargs)


class StudentCreate(GenericAPIView, CreateModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def post(self, request, *args, **kwargs):
        return self.create(self, request, *args, **kwargs)


class StudentUpdate(GenericAPIView, UpdateModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def post(self, request, *args, **kwargs):
        return self.update(self, request, *args, **kwargs)


class StudentDelete(GenericAPIView, DestroyModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def delete(self, request, *args, **kwargs):
        return self.destroy(self, request, *args, **kwargs)


# List And Create : Pk is not Required

class StudentListCreate(GenericAPIView, ListModelMixin, CreateModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


# Read Update Delete : Pk is Required

class StudentRetrieveUpdateDelete(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# Concrete View

class Students(ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentRetrieve(RetrieveAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentsUpdate(UpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentsCreate(CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentsDelete(DestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


# Create and List In Concrete View : pk is Not Required

class StudentCreateList(ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


# Retrieve Delete Update In concrete View : Pk is required

class StudentRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentsApis(viewsets.ViewSet):
    def list(self, request):
        student = Student.objects.all()
        serializer = StudentSerializer(student, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        id = pk
        if id is not None:
            student = Student.objects.get(id=pk)
            serializer = StudentSerializer(student)
            return Response(serializer.data)

    def create(self, request):
        data = request.data
        serializer = StudentSerializer(data)
        if serializer.is_valid():
            return Response({'msg': 'Student Created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        student = Student.objects.get(id=pk)
        data = request.data
        serializer = StudentSerializer(student, data)
        if serializer.is_valid():
            return Response({'msg': 'Student Created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        student = Student.objects.get(id=pk)
        data = request.data
        serializer = StudentSerializer(student, data)
        if serializer.is_valid():
            return Response({'msg': 'Student Created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        student = Student.objects.get(id=pk)
        student.delete()
        Response({'msg': 'Deleted'})


class StudentsApi(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend,SearchFilter]
    filterset_fields = ['name','age']
    search_fields = ['name','age']

