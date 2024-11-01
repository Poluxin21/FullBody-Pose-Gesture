#include <iostream>
#include <openvr.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <cstring>
#include <sstream>
#include <vector>

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
    int sockfd;
    struct sockaddr_in servaddr;

    if ((sockfd = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
        std::cerr << "Erro ao criar socket UDP" << std::endl;
        return -1;
    }

    memset(&servaddr, 0, sizeof(servaddr));
    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = INADDR_ANY;
    servaddr.sin_port = htons(port);

    if (bind(sockfd, (const struct sockaddr *)&servaddr, sizeof(servaddr)) < 0) {
        std::cerr << "Erro ao associar o socket" << std::endl;
        close(sockfd);
        return -1;
    }

    std::cout << "Socket UDP configurado na porta " << port << std::endl;
    return sockfd;
}

// Função para processar e aplicar as coordenadas (x, y, z) no OpenVR
void processAndSendToVR(const std::string &data) {
    std::stringstream ss(data);
    std::vector<float> coords;
    std::string item;

    while (std::getline(ss, item, ',')) {
        try {
            coords.push_back(std::stof(item));
        } catch (const std::invalid_argument& e) {
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
    socklen_t len = sizeof(clientaddr);

    while (true) {
        int n = recvfrom(sockfd, buffer, 1024, MSG_WAITALL, (struct sockaddr *)&clientaddr, &len);
        if (n < 0) {
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
    close(sockfd);
    return 0;
}
