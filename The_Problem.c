#include <stdio.h>
#include <fcntl.h>
#include <errno.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>

#define LOGIN "login"
#define MYFIND "myfind"
#define WC "wc"
#define QUIT "quit"
#define INVALID_COMMAND "Invalid command.\n"
#define INVALID_USERNAME "Invalid username.\n"
#define NOT_LOGGED_IN "Please log in.\n"
#define INVALID_SINTAX "Invalid syntax.\n"
#define MAX_SIZE 100

int main(){
	char command[100],
	     response[100];

	pid_t pid, pid2;
	int fd[2],
	    fd2[2],
	    fileDescriptor,
	    commandLength,
	    responseLength;
	bool loggedIn = false;

	if(pipe(fd) == -1){
		perror("Pipe error.\n");
		exit(2);
	}
	if(pipe(fd2) == -1){
		perror("Pipe error.\n");
		exit(2);
	}
	if((pid = fork()) == -1){
		perror("Fork error.\n");
		exit(3);
	}
	if(pid){
		close(fd[0]);
		close(fd2[1]);
		while(1){
			scanf(" %[^\n]s",command);
			commandLength = strlen(command);
			write(fd[1], &commandLength, sizeof(size_t));
			write(fd[1], command, commandLength);
			memset(response, 0, 100);
			read(fd2[0], &responseLength, sizeof(size_t));
			read(fd2[0], &response, responseLength);
			printf("%s\n", response);
			if(!strcmp(response, QUIT)){
				wait(NULL);
				exit(1);
			}
		}
	}
	else{
		char *cmd = malloc(sizeof(*cmd));
		char tmp[100];
		close(fd[1]);
		close(fd2[0]);
		while(1){
            		memset(command, 0, 100);
			read(fd[0], &commandLength, sizeof(size_t));
			read(fd[0], &command, commandLength);
			strcpy(tmp, command);
			cmd = strtok(tmp, " \n");
			if(!strcmp(cmd, LOGIN)){
				if(!loggedIn){
					char *user = malloc(sizeof(*user));
					char *username = malloc(sizeof(*username));
					char *users = malloc(sizeof(*users));
					username = strchr(command, ' ');
					username += 1;
					fileDescriptor = open("users.txt", O_RDONLY);
					read(fileDescriptor, users, 100);
					close(fileDescriptor);
					user = strtok(users, "\n");
					while(user != NULL){
						if(!strncmp(username,user,strlen(username)-1)){
							loggedIn = true;
							printf("Logged in as %s.\n", user);
							break;
						}
					user = strtok(NULL, "\n");
					}
					if(!loggedIn){
						responseLength = strlen(INVALID_USERNAME);
						write(fd2[1], &responseLength, sizeof(size_t));
						write(fd2[1], INVALID_USERNAME, responseLength);
					}
					free(users);
				}
				else
					printf("Already logged in.\n");
				responseLength = strlen(LOGIN);
				write(fd2[1], &responseLength, sizeof(size_t));
				write(fd2[1], LOGIN, responseLength);
			}
			else if(!strcmp(cmd, MYFIND)){
				if(loggedIn){
					//responseLength = strlen(cmd);
					//write(fd2[1], &responseLength, sizeof(size_t));
					//write(fd2[1], cmd, responseLength);
					char temp[100];
					strcpy(temp, command);
					if((pid2 = fork()) == -1){
						perror("Fork error.\n");
						exit(3);
					}
					if(! pid2){
						if(dup2(fd2[1],1) == -1){
							perror("Redierct error.\n");
							exit(4);
						}
						char *argument;
						argument = strchr(temp, ' ');
						argument += 1;
						int i =100;
						write(fd2[1], &i, sizeof(size_t));
						if(execlp("find", "find", argument, NULL) == -1)
							write(fd2[1], INVALID_SINTAX, MAX_SIZE);
					}
				}
				else{
					responseLength = strlen(NOT_LOGGED_IN);
					write(fd2[1], &responseLength, sizeof(size_t));
					write(fd2[1], NOT_LOGGED_IN, responseLength);
				}
			}
			else if(!strcmp(cmd, WC)){
										if(loggedIn){
					char temp[100];
					strcpy(temp, command);
					//responseLength = strlen(cmd);
					//write(fd2[1], &responseLength, sizeof(size_t));
					//write(fd2[1], cmd, responseLength);
					if((pid2 = fork()) == -1){
						perror("Fork error.\n");
						exit(3);
					}
					if(!pid2){
						if(dup2(fd2[1], 1) == -1){
							perror("Redirect error.\n");
							exit(4);
						}
					char *argument;
						argument = strchr(temp, ' ');
						argument += 1;
						int i =100;
						write(fd2[1], &i, sizeof(size_t));
						if(execlp("wc", "wc", argument, NULL) == -1){
							write(fd2[1], INVALID_SINTAX, responseLength);
						}
					}
				}
				else
					write(fd2[1], NOT_LOGGED_IN, MAX_SIZE);
			}
			else if(!strcmp(cmd, QUIT)){
				responseLength = strlen(QUIT);
				write(fd2[1], &responseLength, sizeof(size_t));
				write(fd2[1], QUIT, responseLength);
				close(fd2[1]);
				exit(1);
			}
			else{
				responseLength = strlen(INVALID_COMMAND);
				write(fd2[1], &responseLength, sizeof(size_t));
				write(fd2[1], INVALID_COMMAND, responseLength);
			}
		}
	}
	return 0;
}
