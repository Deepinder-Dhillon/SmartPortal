from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from clinic.controller import Controller
from clinic.serializers import PatientSerializer
from rest_framework import pagination
from rest_framework.pagination import PageNumberPagination
from rest_framework import status

class PatientPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 100

controller = Controller(autosave=True)

@api_view(['POST'])
@permission_classes([AllowAny])  # Allow all users to call this endpoint
def login(request):
    """Authenticate user and return JWT token"""
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=200)
    return Response({'error': 'Invalid credentials'}, status=401)

@api_view(['POST'])
def logout(request):
    """Blacklist the refresh token to log out"""
    try:
        refresh_token = request.data.get("refresh")
        token = RefreshToken(refresh_token)
        token.blacklist()  # Requires `rest_framework_simplejwt.token_blacklist` to be installed
        return Response({'message': 'Logout successful'}, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_patients(request):
    """Retrieve patients with pagination & backend search"""
    try:
        patients = controller.list_patients(request)


        paginator = PatientPagination()
        paginated_patients = paginator.paginate_queryset(patients, request)

        serializer = PatientSerializer(paginated_patients, many=True)
        return paginator.get_paginated_response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_patients(request):
    """Search patients by name with pagination"""
    try:
        search_query = request.GET.get('search', '')
        patients = controller.retrieve_patients(request, search_query)

        paginator = PatientPagination()
        paginated_patients = paginator.paginate_queryset(patients, request)
        serializer = PatientSerializer(paginated_patients, many=True)

        return paginator.get_paginated_response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=400)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_patient(request):
    """Create a new patient using the controller"""
    try:
        phn = int(request.data.get("phn"))
        name = request.data.get("name")
        birth_date = request.data.get("birthDate")
        phone = request.data.get("phone")
        email = request.data.get("email")
        address = request.data.get("address")

        patient = controller.create_patient(request, phn, name, birth_date, phone, email, address)

        serializer = PatientSerializer(patient)
        return Response({"message": "Patient created successfully", "patient": serializer.data}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_patient(request, original_phn):
    """
    Updates an existing patient.
    - Requires authentication.
    - Calls `controller.update_patient`.
    """
    try:
        data = request.data
        phn = data.get("phn")
        name = data.get("name")
        birth_date = data.get("birth_date")
        phone = data.get("phone")
        email = data.get("email")
        address = data.get("address")

        if not all([phn, name, birth_date, phone, email, address]):
            return Response({"error": "All fields are required."}, status=405)

        success = controller.update_patient(
            request,
            original_phn=int(original_phn),
            phn=int(phn),
            name=name,
            birth_date=birth_date,
            phone=phone,
            email=email,
            address=address
        )

        if success:
            return Response({"message": "Patient updated successfully."}, status=200)
        else:
            return Response({"error": "Failed to update patient."}, status=400)

    except Exception as e:
        return Response({"error": str(e)}, status=401)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_patient(request, phn):
    """Delete a patient by PHN"""
    try:
        success = controller.delete_patient(request, phn)
        if success:
            return Response({'message': 'Patient deleted successfully'}, status=200)
        return Response({'error': 'Patient not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def set_current_patient(request, phn):
    """Set a patient as the current patient (stored in memory)"""
    try:
        controller.set_current_patient(request, int(phn))
        return Response({"message": f"Patient {phn} set as current patient"}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_patient(request):
    """Retrieve the current patient from the controller."""
    try:
        if controller._patient is None:
            return Response({"error": "No current patient set"}, status=404)  # Change 400 to 404

        serializer = PatientSerializer(controller._patient)
        return Response(serializer.data, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unset_current_patient(request):
    """Unset the current patient (clear from memory)"""
    try:
        controller.unset_current_patient(request)
        return Response({"message": "Current patient unset"}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=400)



