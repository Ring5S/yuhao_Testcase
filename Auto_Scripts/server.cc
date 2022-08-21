#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <winsock2.h>
#pragma comment(lib, "ws2_32.lib") // windows 32位版本的，没有64版本的，但是64位下也有32位版本的
#include <unistd.h>
#include <iostream>

#define port 8080 //监听端口，可以在范围内自由设定

using namespace std;

int main()
{
	system("chcp 65001"); // 中文编码
	// 初始化函数必须得有
	WORD wdVersion = MAKEWORD(2, 2); //定义自己需要的网络库版本，这里是2.2
	WSADATA wdSockMsg;				 //这是一个结构体

	int nRes = WSAStartup(wdVersion, &wdSockMsg); //打开一个套接字
												  // 创建套接字
	SOCKET sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
	if (sock == INVALID_SOCKET)
	{
		printf("socket error !");
		return 0;
	}
	cout << "socket ready!" << endl;

	// 2.sockaddr_in结构体：可以存储一套网络地址（包括IP与端口）,此处存储本机IP地址与本地的一个端口
	struct sockaddr_in local_addr;
	// struct sockaddr_in addr;
	auto addr_len = sizeof(local_addr);
	memset((void *)&local_addr, 0, addr_len);
	local_addr.sin_family = AF_INET;
	local_addr.sin_port = htons(port);				//绑定端口
	local_addr.sin_addr.s_addr = htonl(INADDR_ANY); //绑定本机IP地址

	// 3.bind()： 将一个网络地址与一个套接字绑定，此处将本地地址绑定到一个套接字上
	int res = bind(sock, (struct sockaddr *)&local_addr, sizeof(local_addr));
	std::cout << res << std::endl;
	if (res == -1)
	{
		cout << "bind error!" << endl;
		exit(-1);
	}
	cout << "bind ready!" << endl;

	// 4.listen()函数：监听试图连接本机的客户端
	//参数二：监听的进程数
	if (listen(sock, 10) == SOCKET_ERROR)
	{
		cout << "Listen error" << endl;
		return 1;
	}
	int time = 1;
	// 5.创建一个sockaddr_in结构体，用来存储客户机的地址
	sockaddr_in client_addr;
	char msg[1024]; //存储传送的消息
	int len = sizeof(client_addr);
	int flag = 0; //是否已经连接上
	while (true) //循环接收客户端的请求
	{
		time ++;
		// 6.accept()函数：阻塞运行，直到收到某一客户机的连接请求，并返回客户机的描述符
		SOCKET client_fd = accept(sock, (struct sockaddr *)&client_addr, &len);
		if (!flag)
		{
			cout << "等待来自客户端的连接..." << endl;
		}
		if (client_fd == INVALID_SOCKET)
		{
			cout << "accept Error\n"
				 << endl;
			exit(-1);
		}
		// 7.输出客户机的信息
		char *ip = inet_ntoa(client_addr.sin_addr);
		if (!flag)
		{
			cout << "接收到一个链接：" << ip << endl;
		}
		// flag = 1;
		int num = recv(client_fd, msg, 100, 0);
		if (num > 0)
		{
			msg[num] = '\0';
			cout << "Client say: " << msg << endl;
		}
		std::string str_time = std::to_string(time);
		char html[1024];
		string init_text = "HTTP/1.1 200 OK\r\nContent-type: text/html\r\n\r\nTime of MS is " + str_time;
		strcpy(html,init_text.c_str());

		int size = send(client_fd, html, strlen(html), 0);
		// flag = 0;
		closesocket(client_fd);
		// continue;
	}

	closesocket(sock);
	WSACleanup();
}
