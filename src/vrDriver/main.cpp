#include <iostream>
#include <openvr.h>
#include <winsock2.h>
#include <ws2tcpip.h>
#include <sstream>
#include <vector>

#pragma comment(lib, "Ws2_32.lib") // Link the Winsock library

vr::IVRSystem* vrSystem = nullptr;

// Inicializa o OpenVR
bool initOpenVR() {
    vr::EVRInitError error = vr::VRInitError_None;
    vrSystem = vr::VR_Init(&error, vr::VRApplication_Scene);

    if (error != vr::VRInitError_None) {
        std::cerr << "Erro ao inicializar o OpenVR: " << vr::VR_GetVRInitErrorAsEnglishDescription(error) << std::endl;
        return false;
    }

    std::cout << "OpenVR inicializado com sucesso." << std::endl;
    return true;
}

// Configura o socket UDP para receber os dados
int setupUDPSocket(int port) {
    SOCKET sockfd;
    struct sockaddr_in servaddr;

    WSADATA wsaData;
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        std::cerr << "Erro ao inicializar o Winsock" << std::endl;
        return -1;
    }

    if ((sockfd = socket(AF_INET, SOCK_DGRAM, 0)) == INVALID_SOCKET) {
        std::cerr << "Erro ao criar socket UDP" << std::endl;
        WSACleanup();
        return -1;
    }

    memset(&servaddr, 0, sizeof(servaddr));
    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = INADDR_ANY;
    servaddr.sin_port = htons(port);

    if (bind(sockfd, (const struct sockaddr*)&servaddr, sizeof(servaddr)) == SOCKET_ERROR) {
        std::cerr << "Erro ao associar o socket" << std::endl;
        closesocket(sockfd);
        WSACleanup();
        return -1;
    }

    std::cout << "Socket UDP configurado na porta " << port << std::endl;
    return sockfd;
}

// Função para processar e aplicar as coordenadas (x, y, z) no OpenVR
void processAndSendToVR(const std::string& data) {
    std::stringstream ss(data);
    std::vector<float> coords;
    std::string item;

    while (std::getline(ss, item, ',')) {
        try {
            coords.push_back(std::stof(item));
        }
        catch (const std::invalid_argument& e) {
            std::cerr << "Erro ao converter coordenadas: " << e.what() << std::endl;
            return;
        }
    }

    if (coords.size() == 3) {
        float x = coords[0];
        float y = coords[1];
        float z = coords[2];
        std::cout << "Coordenadas recebidas: x=" << x << " y=" << y << " z=" << z << std::endl;

        // Falta adicionar codigo para processar info
    }
}

void receiveDataAndSendToVR(int sockfd) {
    char buffer[1024];
    struct sockaddr_in clientaddr;
    int len = sizeof(clientaddr);

    while (true) {
        int n = recvfrom(sockfd, buffer, sizeof(buffer) - 1, 0, (struct sockaddr*)&clientaddr, &len);
        if (n == SOCKET_ERROR) {
            std::cerr << "Erro ao receber dados no socket UDP" << std::endl;
            continue;
        }

        buffer[n] = '\0';
        std::string data(buffer);
        processAndSendToVR(data);
    }
}

int main() {
    if (!initOpenVR()) {
        return -1;
    }

    int udpPort = 5052;
    int sockfd = setupUDPSocket(udpPort);

    if (sockfd < 0) {
        vr::VR_Shutdown();
        return -1;
    }

    receiveDataAndSendToVR(sockfd);

    vr::VR_Shutdown();
    closesocket(sockfd);
    WSACleanup(); // Limpa o Winsock
    return 0;
}
