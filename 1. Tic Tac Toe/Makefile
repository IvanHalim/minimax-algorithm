CXX = g++
SRCS = main.cpp game.cpp AI.cpp
HEADERS = game.hpp AI.hpp
OBJS = main.o game.o AI.o
game: ${OBJS} ${HEADERS}
	${CXX} ${OBJS} -o game
${OBJS}: ${SRCS}
	${CXX} -c $(@:.o=.cpp)
clean:
	rm -f *.o game
