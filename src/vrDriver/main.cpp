#include <iostream>
#include <openvr.h>

// Inicialização do OpenVR
bool initOpenVR()
{
    vr::EVRInitError error = vr::VRInitError_None;
    vr::IVRSystem *vrSystem = vr::VR_Init(&error, vr::VRApplication_Scene);
}


int main() {

}