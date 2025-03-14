from app import create_app, db
import socket

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    # 打印本机 IP 地址，方便确认
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    print(f"Server running at: http://{local_ip}:5001/docs")
    
    # 确保监听所有网络接口
    app.run(
        host='0.0.0.0',  # 监听所有网络接口
        port=5001,
        debug=True
    )