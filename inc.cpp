#include <SFML/Graphics.hpp>
#include <opencv2/opencv.hpp>
#include <iostream>

using namespace sf;
using namespace cv;

const int WIDTH = 800, HEIGHT = 500;
const float PADDLE_SPEED = 5.0f, BALL_SPEED = 4.0f;

int main() {
    RenderWindow window(VideoMode(WIDTH, HEIGHT), "Table Tennis Game");
    
    // Table and Net
    RectangleShape table(Vector2f(WIDTH, HEIGHT));
    table.setFillColor(Color::Green);
    RectangleShape net(Vector2f(10, HEIGHT));
    net.setPosition(WIDTH / 2 - 5, 0);
    net.setFillColor(Color::White);
    
    // Paddles and Ball
    RectangleShape playerPaddle(Vector2f(10, 80)), compPaddle(Vector2f(10, 80)), ball(Vector2f(10, 10));
    playerPaddle.setFillColor(Color::Blue);
    compPaddle.setFillColor(Color::Red);
    ball.setFillColor(Color::White);
    
    playerPaddle.setPosition(50, HEIGHT / 2 - 40);
    compPaddle.setPosition(WIDTH - 60, HEIGHT / 2 - 40);
    ball.setPosition(WIDTH / 2, HEIGHT / 2);
    
    float ball_dx = BALL_SPEED, ball_dy = BALL_SPEED;
    VideoCapture cap(0);
    if (!cap.isOpened()) {
        std::cout << "Error: Camera not detected!" << std::endl;
        return -1;
    }
    
    while (window.isOpen()) {
        Event event;
        while (window.pollEvent(event)) {
            if (event.type == Event::Closed)
                window.close();
        }
        
        // Capture frame for hand tracking
        Mat frame;
        cap >> frame;
        flip(frame, frame, 1);
        cvtColor(frame, frame, COLOR_BGR2GRAY);
        
        // Simple thresholding for hand detection (Modify for better accuracy)
        threshold(frame, frame, 128, 255, THRESH_BINARY);
        Moments m = moments(frame);
        if (m.m00 > 0) {
            int handY = static_cast<int>(m.m01 / m.m00);
            playerPaddle.setPosition(50, handY - 40);
        }
        
        // AI Paddle Movement
        if (ball.getPosition().y < compPaddle.getPosition().y + 40)
            compPaddle.move(0, -PADDLE_SPEED);
        else if (ball.getPosition().y > compPaddle.getPosition().y + 40)
            compPaddle.move(0, PADDLE_SPEED);
        
        // Ball Movement
        ball.move(ball_dx, ball_dy);
        
        if (ball.getPosition().y <= 0 || ball.getPosition().y >= HEIGHT - 10)
            ball_dy = -ball_dy;
        if (ball.getGlobalBounds().intersects(playerPaddle.getGlobalBounds()) || ball.getGlobalBounds().intersects(compPaddle.getGlobalBounds()))
            ball_dx = -ball_dx;
        
        window.clear();
        window.draw(table);
        window.draw(net);
        window.draw(playerPaddle);
        window.draw(compPaddle);
        window.draw(ball);
        window.display();
    }
    return 0;
}
