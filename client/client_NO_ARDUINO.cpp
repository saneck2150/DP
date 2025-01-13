#include <iostream>
#include <string>
#include <cstring>
#include <arpa/inet.h>
#include <unistd.h>

// Encryption class
class Encryptor {
public:
    static std::string encrypt(const std::string& data) {
        std::string encrypted = data;
        for (char& c : encrypted) {
            c ^= 0xAA; // Simple XOR encryption with a key (0xAA).
        }
        return encrypted;
    }
};

// TCP Client class
class TcpClient {
private:
    int sock;
    struct sockaddr_in server_address;

public:
    TcpClient(const std::string& ip, int port) {
        sock = socket(AF_INET, SOCK_STREAM, 0);
        if (sock < 0) {
            throw std::runtime_error("Socket creation failed");
        }

        server_address.sin_family = AF_INET;
        server_address.sin_port = htons(port);

        if (inet_pton(AF_INET, ip.c_str(), &server_address.sin_addr) <= 0) {
            throw std::runtime_error("Invalid IP address");
        }
    }

    void connectToServer() {
        if (connect(sock, (struct sockaddr*)&server_address, sizeof(server_address)) < 0) {
            throw std::runtime_error("Connection to server failed");
        }
        std::cout << "Connected to server." << std::endl;
    }

    void sendMessage(const std::string& message) {
        std::string encryptedMessage = Encryptor::encrypt(message);
        if (send(sock, encryptedMessage.c_str(), encryptedMessage.size(), 0) < 0) {
            throw std::runtime_error("Failed to send message");
        }
        std::cout << "Message sent: " << message << std::endl;
    }

    ~TcpClient() {
        close(sock);
    }
};

int main() {
    try {
        TcpClient client("127.0.0.1", 12345);
        client.connectToServer();

        std::string message = "1234567890";
        client.sendMessage(message);
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
    }

    return 0;
}
