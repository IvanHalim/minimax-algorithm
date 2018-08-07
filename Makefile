CXX = g++
SRCS = main.cpp game.cpp
HEADERS = game.hpp
OBJS = main.o game.o
game: ${OBJS} ${HEADERS}
	${CXX} ${OBJS} -o game
${OBJS}: ${SRCS}
	${CXX} -c $(@:.o=.cpp)
clean:
	rm -f *.o game
