from flask import Flask, render_template, request, redirect, jsonify, url_for, session, flash
from flask_mysqldb import MySQL
from flask import send_from_directory
import requests




import os
from datetime import datetime
import bcrypt
import random
import threading


app = Flask(__name__)


# 定义上传文件保存路径
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 定义生成唯一文件名的函数，通过当前时间戳和随机数来保证文件名的唯一性。
def generate_unique_filename(filename):
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    random_num = str(random.randint(1000, 9999))
    _, file_extension = os.path.splitext(filename)
    unique_filename = f"{timestamp}_{random_num}{file_extension}"
    return unique_filename



# 生成下一个可用的4位数会员ID，从5000开始
# 初始的 member_id，建议设置为4999，因为您希望从5000开始
# 初始的 member_id
current_member_id = 4999

# 为会话管理设置秘密密钥
app.secret_key = 'your_secret_key'  # 替换为您的秘密密钥

def generate_member_id():
    global current_member_id
    lock = threading.Lock()
    with lock:
        current_member_id += 1
        if current_member_id > 9999:
            current_member_id = 5000
        return str(current_member_id)

# 注册路由保持不变，只是使用新的 generate_member_id 函数

# MySQL 配置
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'LIANG1009'
app.config['MYSQL_DB'] = 'your_database_name'  # 请替换为您的数据库名
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'



# 初始化 MySQL
mysql = MySQL(app)

# 为会话管理设置秘密密钥
app.secret_key = 'your_secret_key'  # 请替换为您的秘密密钥




# 首页路由
@app.route('/')
def index():
    # 如果未登录，渲染未登录首页模板
    if 'username' not in session:
        return render_template('home.html')

    # 如果已登录，渲染登录后首页模板并传递用户名参数
    username = session['username']
    return render_template('home.html', username=username)


# 登录后首页路由
@app.route('/home')
def home():
    if 'username' in session:
        username = session['username']
        cur = mysql.connection.cursor()

        try:
            # 查询用户的钱包余额
            cur.execute("SELECT balance FROM wallets WHERE user_id = (SELECT id FROM users WHERE username = %s)",
                        (username,))
            balance_result = cur.fetchone()
            balance = balance_result['balance'] if balance_result else None

            # 查询用户的会员号ID
            cur.execute("SELECT member_id FROM users WHERE username = %s", (username,))
            member_id_result = cur.fetchone()
            member_id = member_id_result['member_id'] if member_id_result else None



            cur.close()

            # 渲染主页模板并传递用户名、余额和会员号ID
            return render_template('home.html', username=username, balance=balance, member_id=member_id)

        except Exception as e:
            cur.close()
            return "发生错误：{}".format(str(e))

    return redirect(url_for('login'))  # 如果用户未登录，则重定向到登录页面


from flask import flash

# ... 其他代码 ...


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            # 从表单中获取用户信息
            userDetails = request.form
            username = userDetails['username']
            password = userDetails['password']
            wechat = userDetails.get('wechat', '')
            email = userDetails.get('email', '')
            phone = userDetails.get('phone', '')

            # 密码加密
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            # 生成会员ID
            member_id = generate_member_id()

            # 使用数据库事务确保数据一致性
            with mysql.connection.cursor() as cursor:
                # 向数据库插入用户信息
                cursor.execute(
                    "INSERT INTO users (username, password, wechat, email, phone, member_id) VALUES (%s, %s, %s, %s, %s, %s)",
                    (username, hashed_password, wechat, email, phone, member_id)
                )
                mysql.connection.commit()

                # 获取新插入的用户ID
                user_id = cursor.lastrowid

                # 插入钱包记录，注意这里不需要手动插入id，因为它是自增主键
                cursor.execute(
                    "INSERT INTO wallets (user_id, balance, member_id) VALUES (%s, %s, %s)",
                    (user_id, 0.00, member_id)  # 初始余额设置为0.00
                )
                mysql.connection.commit()  # 提交事务



                # 假设：创建用户钱包记录的逻辑（如果有）

            session['username'] = username  # 将用户名存储在会话中
            flash('注册成功，请登录。', 'success')
            return redirect(url_for('login'))  # 注册成功后重定向到登录页面

        except Exception as e:
            app.logger.error(f"注册失败：{e}")
            flash(f'注册失败：{e}', 'error')
            # 在捕获异常时返回错误页面
            return render_template('register.html'), 400  # 返回 400 错误状态码

    # 如果是GET请求，渲染注册页面
    return render_template('register.html')
# 登录页面路由
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identity = request.form['identity']
        password = request.form['password'].encode('utf-8')

        # 尝试使用 identity 查找用户，无论是 member_id 还是 username
        user = find_user_by_identity(identity)

        # 如果用户存在且密码匹配，则登录成功
        if user and bcrypt.checkpw(password, user['password'].encode('utf-8')):
            # 存储 username 到会话
            session['username'] = user['username']
            flash('登录成功！', 'success')
            return redirect(url_for('home'))
        else:
            flash('无效的身份标识或密码。', 'error')

    return render_template('login.html')

def find_user_by_identity(identity):
    cur = mysql.connection.cursor()
    # 尝试匹配 member_id
    cur.execute("SELECT * FROM users WHERE member_id = %s", (identity,))
    user = cur.fetchone()
    if not user:
        # 如果 member_id 未找到用户，则尝试匹配 username
        cur.execute("SELECT * FROM users WHERE username = %s", (identity,))
        user = cur.fetchone()
    return user


# 退出登录路由
@app.route('/logout')
def logout():
    session.pop('username', None)  # 从会话中移除用户名
    flash('退出登录成功！', 'success')  # 提示退出登录成功
    return redirect(url_for('login'))  # 退出登录后重定向到首页


# 添加包裹页面路由
@app.route('/add_package', methods=['GET', 'POST'])
def add_package():
    if 'username' in session:  # 检查用户是否登录
        username = session['username']
        cur = mysql.connection.cursor()

        # 查询当前用户的会员 ID
        cur.execute("SELECT member_id FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        member_id = user['member_id']

        if request.method == 'POST':
            # 获取表单提交的包裹信息
            warehouse_name = request.form.get('warehouse_name', '')
            item_name = request.form.get('item_name', '')
            weight = request.form.get('weight', None) if request.form.get('weight', None) != '' else None
            size = request.form.get('size', '')
            quantity = request.form.get('quantity', None) if request.form.get('quantity', None) != '' else None
            status = request.form.get('status', '未入库')
            tracking_number = request.form.get('tracking_number', '')
            courier_company = request.form.get('courier_company', '')
            note = request.form.get('note', '')
            cargo_type = request.form.get('cargo_type', '普货')

            # 执行插入包裹信息的 SQL 查询
            cur.execute(
                "INSERT INTO packages (member_id, warehouse_name, item_name, weight, size, quantity, status, tracking_number, courier_company, note, cargo_type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (member_id, warehouse_name, item_name, weight, size, quantity, status, tracking_number, courier_company, note, cargo_type)
            )

            mysql.connection.commit()  # 提交事务
            flash('包裹信息提交成功', 'success')  # 提示包裹信息提交成功
            return redirect(url_for('my_packages'))  # 提交成功后重定向到我的包裹

        else:
            # 查询已有的仓库名称列表
            cur.execute("SELECT warehouse_name FROM warehouses")
            warehouse_names = [row['warehouse_name'] for row in cur.fetchall()]  # 获取仓库名称列表

            # 关闭游标
            cur.close()

            # 将仓库名称列表传递给 HTML 模板
            return render_template('add_package.html', warehouse_names=warehouse_names)

    else:
        return redirect(url_for('login'))  # 如果用户未登录，则重定向到登录页面


# 添加批量添加包裹页面的路由
@app.route('/batch_add_packages', methods=['GET', 'POST'])
def batch_add_packages():
    if 'username' in session:  # 检查用户是否登录
        username = session['username']
        cur = mysql.connection.cursor()

        # 查询当前用户的会员 ID
        cur.execute("SELECT member_id FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        member_id = user['member_id']

        if request.method == 'POST':
            # 获取用户输入的快递单号
            tracking_numbers = request.form.get('tracking_numbers', '')
            # 分割用户输入的快递单号，使用换行符分隔
            individual_numbers = tracking_numbers.split('\n')

            # 将每个快递单号插入到数据库中
            for tracking_number in individual_numbers:
                # 执行插入包裹信息的 SQL 查询
                cur.execute(
                    "INSERT INTO packages (member_id, tracking_number) VALUES (%s, %s)",
                    (member_id, tracking_number.strip())# 去除可能存在的前后空格
                 )


            mysql.connection.commit()  # 提交事务
            flash('快递单号提交成功', 'success')  # 提示快递单号提交成功
            return redirect(url_for('my_packages'))  # 提交成功后重定向到我的包裹

        else:
            # 查询已有的仓库名称列表
            cur.execute("SELECT warehouse_name FROM warehouses")
            warehouse_names = [row['warehouse_name'] for row in cur.fetchall()]  # 获取仓库名称列表

            # 关闭游标
            cur.close()

            # 将仓库名称列表传递给 HTML 模板
            return render_template('batch_add_packages.html', warehouse_names=warehouse_names)

    else:
        return redirect(url_for('login'))  # 如果用户未登录，则重定向到登录页面



# 查看用户的包裹信息页面路由
@app.route('/my_packages')
def my_packages():
    if 'username' in session:
        username = session['username']
        cur = mysql.connection.cursor()
        # 查询用户的会员ID
        cur.execute("SELECT member_id FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        member_id = user['member_id']
        # 查询用户的所有包裹信息，包括 cargo_type 字段
        cur.execute("SELECT id, item_name, weight, size, status, quantity, note, tracking_number, courier_company, cargo_type FROM packages WHERE member_id = %s", (member_id,))

        packages = cur.fetchall()
        cur.close()
        return render_template('my_packages.html', packages=packages)
    else:
        return redirect(url_for('login'))  # 如果用户未登录，则重定向到登录页面





# 查看用户未入库包裹信息页面路由
@app.route('/my_not_stored_packages')
def my_not_stored_packages():
    if 'username' in session:
        username = session['username']
        cur = mysql.connection.cursor()
        # 查询用户的会员ID
        cur.execute("SELECT member_id FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        member_id = user['member_id']
        # 查询用户状态为未入库的包裹信息，包括 cargo_type 字段
        cur.execute("""
            SELECT id, item_name, weight, size, status, quantity, note, tracking_number, courier_company, cargo_type 
            FROM packages 
            WHERE member_id = %s AND status = %s
        """, (member_id, '未入库'))

        packages = cur.fetchall()
        cur.close()
        return render_template('my_not_stored_packages.html', packages=packages)
    else:
        return redirect(url_for('login'))  # 如果用户未登录，则重定向到登录页面

# 删除包裹路由
@app.route('/delete_package', methods=['POST'])
def delete_package():
    if 'username' in session:
        package_id = request.json['id']  # 从 JSON 数据中获取要删除的包裹的 ID
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM packages WHERE id = %s", (package_id,))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Package deleted successfully'}), 200
    else:
        return jsonify({'error': 'User not authenticated'}), 401


# 查看用户已入库包裹信息页面路由
@app.route('/my_stored_packages')
def my_stored_packages():
    if 'username' in session:
        username = session['username']
        cur = mysql.connection.cursor()
        # 查询用户的会员ID
        cur.execute("SELECT member_id FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        member_id = user['member_id']
        # 查询用户状态为未入库的包裹信息，包括 cargo_type 字段
        cur.execute("""
            SELECT id, item_name, weight, size, status, quantity, note, tracking_number, courier_company, cargo_type 
            FROM packages 
            WHERE member_id = %s AND status = %s
        """, (member_id, '已入库'))

        packages = cur.fetchall()
        cur.close()
        return render_template('my_stored_packages.html', packages=packages)
    else:
        return redirect(url_for('login'))  # 如果用户未登录，则重定向到登录页面

# 查看仓库地址数据页面路由
@app.route('/warehouse_addresses')
def warehouse_addresses():
    if 'username' in session:
        username = session['username']
        cur = mysql.connection.cursor()

        # 查询用户的会员号ID
        cur.execute("SELECT member_id FROM users WHERE username = %s", (username,))
        member_id_result = cur.fetchone()
        member_id = member_id_result['member_id'] if member_id_result else None




        # 查询仓库地址数据
        cur.execute("SELECT warehouse_name, warehouse_address, warehouse_contact_person, warehouse_phone_number, warehouse_postcode FROM warehouses")
        rows = cur.fetchall()

        # 将结果转换为字典类型列表
        warehouse_data = []
        for row in rows:
            warehouse_data.append({
                'warehouse_name': row['warehouse_name'],
                'warehouse_address': row['warehouse_address'],
                'warehouse_contact_person': row['warehouse_contact_person'],
                'warehouse_phone_number': row['warehouse_phone_number'],
                'warehouse_postcode': row['warehouse_postcode']
            })


        # 关闭游标
        cur.close()

        # 渲染模板并传递数据
        return render_template('warehouse_addresses.html', warehouse_data=warehouse_data,member_id=member_id)
    else:
        return redirect(url_for('login'))  # 如果用户未登录，则重定向到登录页面

# 确保您有 login 和 index 路由定义在其他地方

@app.route('/add_address', methods=['GET', 'POST'])
def add_address():
    if request.method == 'POST':
        # 从表单获取数据
        userDetails = request.form
        name = userDetails['name']
        address = userDetails['address']
        phone = userDetails['phone']
        postcode = userDetails['postcode']
        city = userDetails['city']
        member_id = userDetails['member_id']  # 获取 member_id

        # 获取当前登录用户的用户名
        if 'username' in session:
            username = session['username']

            # 将地址信息及 member_id 保存到数据库中
            cursor = mysql.connection.cursor()
            cursor.execute(
                "INSERT INTO addresses (username, member_id, name, address, phone, postcode, city) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (username, member_id, name, address, phone, postcode, city)
            )
            mysql.connection.commit()
            cursor.close()

            flash('地址添加成功', 'success')
            return redirect(url_for('my_addresses'))  # 添加成功后重定向到地址管理页面

        else:
            return redirect(url_for('login'))

    else:
        # 如果是GET请求，获取当前登录用户的详细信息并渲染模板
        if 'username' in session:
            username = session['username']
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user_info = cursor.fetchone()
            cursor.close()
            return render_template('add_address.html', user_info=user_info)

        else:
            return redirect(url_for('login'))

    return render_template('add_address.html')
# 我的地址管理页面路由
# 我的地址管理页面路由
@app.route('/my_addresses')
def my_addresses():
    if 'username' in session:
        username = session['username']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM addresses WHERE username = %s", (username,))
        addresses = cur.fetchall()
        cur.close()
        return render_template('my_addresses.html', addresses=addresses)
    else:
        return redirect(url_for('login'))  # 如果用户未登录，则重定向到登录页面


@app.route('/edit_address/<int:address_id>', methods=['GET'])
def edit_address_page(address_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM addresses WHERE id = %s", (address_id,))
    address = cur.fetchone()
    cur.close()
    if address:
        # 将地址数据传递给模板
        return render_template('edit_address.html', address=address)
    else:
        # 如果没有找到地址，返回404
        return jsonify({'status': 'error', 'message': 'Address not found'}), 404


@app.route('/edit_address', methods=['POST'])
def edit_address():
    address_id = request.form.get('address_id')
    if not address_id:
        return jsonify({'status': 'error', 'message': 'No address ID provided'}), 400

    # 获取表单数据
    new_name = request.form.get('name')
    new_address = request.form.get('address')
    new_phone = request.form.get('phone')
    new_postcode = request.form.get('postcode')
    new_city = request.form.get('city')

    if not all([new_name, new_address, new_phone, new_postcode, new_city]):
        return jsonify({'status': 'error', 'message': 'Missing form data'}), 400

    cur = mysql.connection.cursor()
    try:
        cur.execute(
            "UPDATE addresses SET name = %s, address = %s, phone = %s, postcode = %s, city = %s WHERE id = %s",
            (new_name, new_address, new_phone, new_postcode, new_city, address_id)
        )
        mysql.connection.commit()  # 确保提交事务
        cur.close()
        return redirect(url_for('my_addresses'))  # 重定向到地址列表页面
    except Exception as e:
        cur.close()
        # 记录错误信息到日志
        # app.logger.error(f"Failed to update address {address_id}: {e}")
        return jsonify({'status': 'error', 'message': 'Internal server error'}), 500

@app.route('/delete_address', methods=['POST'])
def delete_address():
    if 'username' in session:
        address_id = request.form.get('address_id')
        if address_id:
            cur = mysql.connection.cursor()
            try:
                cur.execute("DELETE FROM addresses WHERE id = %s", (address_id,))
                mysql.connection.commit()  # 确保提交事务
                result = cur.rowcount  # 获取受影响的行数
                cur.close()
                if result > 0:
                    return jsonify({'status': 'success'}), 200
                else:
                    return jsonify({'status': 'error', 'message': '地址不存在'}), 404
            except Exception as e:
                cur.close()
                return jsonify({'status': 'error', 'message': str(e)}), 500
        else:
            return jsonify({'status': 'error', 'message': '未提供地址ID'}), 400
    else:
        return jsonify({'status': 'error', 'message': '用户未登录'}), 401
# 查看已入库状态包裹路由
@app.route('/view_processed_packages')
def view_processed_packages():
    if 'username' in session:
        username = session['username']
        cur = mysql.connection.cursor()
        # 查询用户的会员ID
        cur.execute("SELECT member_id FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        member_id = user['member_id']
        # 查询已入库状态的包裹信息
        cur.execute("SELECT id, item_name, weight, size, status, quantity, note, tracking_number, courier_company FROM packages WHERE member_id = %s AND status = '已入库'", (member_id,))
        processed_packages = cur.fetchall()
        cur.close()
        return render_template('processed_packages.html', processed_packages=processed_packages)
    else:
        return redirect(url_for('login'))  # 如果用户未登录，则重定向到登录页面


@app.route('/create_order', methods=['GET', 'POST'])
def create_order():
    # 检查用户是否登录
    if 'username' not in session:
        return redirect(url_for('login'))  # 如果用户未登录，则重定向到登录页面

    if request.method == 'POST':
        # 获取订单信息
        order_details = request.form
        tracking_numbers = order_details.getlist('tracking_numbers')  # 获取选中的包裹快递单号列表
        shipping_address = order_details['shipping_address']  # 获取收货地址
        city = order_details['city']  # 获取城市
        delivery_method = order_details['delivery_method']  # 获取运输方式
        courier_company = order_details['courier_company']  # 获取快递公司
        is_sensitive = '敏感货' if 'is_sensitive' in order_details else '普通货'  # 获取是否为敏感货
        remarks = order_details['remarks']  # 获取备注信息

        # 获取当前登录用户的用户ID和会员ID
        username = session['username']
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, member_id FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        user_id = user['id']
        member_id = user['member_id']

        # 创建新订单并获取订单ID
        cur.execute(
            "INSERT INTO orders (user_id, member_id, tracking_number, shipping_address, city, delivery_method, courier_company, is_sensitive, remarks, order_status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (user_id, member_id, "your_tracking_number_here", shipping_address, city, delivery_method, courier_company, is_sensitive, remarks, '待处理'))

        mysql.connection.commit()  # 提交事务，保存修改到数据库
        order_id = cur.lastrowid  # 获取新创建订单的ID

        # 将选中的包裹与新创建的订单关联起来
        for tracking_number in tracking_numbers:
            cur.execute("UPDATE packages SET order_id = %s WHERE tracking_number = %s",
                        (order_id, tracking_number))
            mysql.connection.commit()  # 提交事务，保存修改到数据库

        flash('订单创建成功', 'success')  # 显示成功消息
        return redirect(url_for('pending_review_orders'))  # 重定向到主页

    # 如果请求方法为GET，则渲染订单创建页面
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM packages WHERE status = '已入库'")
    processed_packages = cur.fetchall()  # 获取已入库的包裹信息
    return render_template('create_order.html', processed_packages=processed_packages)  # 渲染订单创建页面，传递已入库的包裹信息


# 定义路由函数，当用户访问'/select_packages'这个URL时，会触发这个函数
# 定义路由函数，当用户访问'/select_packages'这个URL时，会触发这个函数
# 允许使用GET和POST请求方法
@app.route('/select_packages', methods=['GET', 'POST'])
def select_packages():
    # 检查用户是否已经登录
    if 'username' not in session:
        flash('您还没有登录，请先登录。', 'warning')
        return redirect(url_for('login'))  # 重定向到登录页面

    # 获取当前登录用户的用户名
    username = session['username']

    # 初始化包裹列表
    processed_packages = None

    try:
        # 创建数据库连接的游标对象
        cur = mysql.connection.cursor()
        # 查询当前登录用户的 member_id
        cur.execute("SELECT member_id FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        if user:
            member_id = user['member_id']
            # 根据 member_id 查询状态为“已入库”的包裹信息
            cur.execute("SELECT * FROM packages WHERE member_id = %s AND status = '已入库'", (member_id,))
            processed_packages = cur.fetchall()  # 获取查询结果
        else:
            flash('用户未找到或会话失效，请重新登录。', 'error')
            return redirect(url_for('home'))  # 用户未找到或会话失效

        cur.close()
    except Exception as e:
        # 记录错误日志
        app.logger.error("An error occurred while fetching member_id or packages from the database: %s", str(e))
        # 显示错误提示信息
        flash('查询包裹信息失败，请稍后再试。', 'error')
        return redirect(url_for('home'))  # 重定向到首页

    # 处理 POST 请求
    if request.method == 'POST':
        selected_packages = request.form.getlist('selected_packages')
        session['selected_packages'] = selected_packages
        return redirect(url_for('fill_order_info'))  # 重定向到填写订单信息页面

    # 如果是 GET 请求，渲染模板并传递包裹列表
    return render_template('select_packages.html', processed_packages=processed_packages)


@app.route('/select_address', methods=['GET', 'POST'])
def select_address():
    """
    处理选择地址的路由。

    如果请求方法为POST：
        - 获取用户选择的地址ID，并存储在会话中。
        - 重定向到填写订单信息页面。

    如果请求方法为GET：
        - 从数据库中获取当前用户的所有地址。
        - 渲染选择地址页面，并将地址信息传递给模板。
    """
    # 检查用户是否登录
    if 'username' not in session:
        flash('请先登录。', 'warning')
        return redirect(url_for('login'))

    if request.method == 'POST':
        # 如果请求方法是POST，获取用户选择的地址ID
        selected_address = request.form.get('selected_address')

        # 将选择的地址ID存储在会话中
        session['selected_address'] = selected_address

        # 重定向到填写订单信息页面
        return redirect(url_for('fill_order_info'))
    else:
        try:
            # 如果请求方法是GET，从数据库中获取当前用户的所有地址
            username = session['username']
            cur = mysql.connection.cursor()
            cur.execute("SELECT member_id FROM users WHERE username = %s", (username,))
            user = cur.fetchone()

            if not user:
                flash('用户信息获取失败，请重新登录。', 'error')
                return redirect(url_for('login'))

            member_id = user['member_id']
            cur.execute("SELECT * FROM addresses WHERE member_id = %s", (member_id,))
            addresses = cur.fetchall()

            # 关闭数据库游标
            cur.close()

            # 渲染选择地址页面，并将地址信息传递给模板
            return render_template('select_address.html', addresses=addresses)
        except Exception as e:
            # 如果发生异常，记录错误信息到日志中
            app.logger.error("从数据库获取地址时发生错误: %s", str(e))

            # 显示错误信息给用户，并重定向到主页
            flash('发生错误。请稍后再试。', 'error')
            return redirect(url_for('home'))



@app.route('/fill_order_info', methods=['GET', 'POST'])
def fill_order_info():
    # 检查用户是否登录
    if 'username' not in session:
        flash('请先登录', 'error')
        return redirect(url_for('login'))

    # 在 try 语句块开始之前创建游标
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        # 从表单中获取订单详情
        order_details = request.form
        address_id = order_details['address']
        delivery_method = order_details['delivery_method']
        courier_company = order_details['courier_company']
        cargo_type = order_details['cargo_type']
        remark = order_details.get('备注', '')

        username = session['username']

        # 获取用户ID和会员ID
        cur.execute("SELECT id, member_id FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        user_id = user['id']
        member_id = user['member_id']

        # 获取选择的地址信息
        cur.execute("SELECT * FROM addresses WHERE id = %s", (address_id,))
        address_info = cur.fetchone()
        shipping_address = address_info['address']
        city = address_info['city']
        phone_number = address_info['phone']
        recipient_name = address_info['name']

        # 插入订单信息
        cur.execute(
            "INSERT INTO orders (user_id, member_id, tracking_number, shipping_address, city, delivery_method, courier_company, is_sensitive, remarks, order_status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (user_id, member_id, "your_tracking_number_here", shipping_address, city, delivery_method, courier_company,
             cargo_type, remark, '待处理'))
        mysql.connection.commit()
        order_id = cur.lastrowid

        # 更新包裹信息
        for tracking_number in session.get('selected_packages', []):
            cur.execute("UPDATE packages SET order_id = %s, status = '待处理'WHERE tracking_number = %s", (order_id, tracking_number))
        mysql.connection.commit()

        print("订单提交成功！订单ID：", order_id)  # 打印提交成功的消息, status = '待处理'

        flash('订单创建成功', 'success')
        return redirect(url_for('pending_review_orders'))

    else:
        # 获取所有地址信息
        cur.execute("SELECT * FROM addresses")
        addresses = cur.fetchall()

        # 获取选中的地址信息
        selected_address_id = session.get('selected_address')
        cur.execute("SELECT * FROM addresses WHERE id = %s", (selected_address_id,))
        selected_address = cur.fetchone()

        # 获取选中的包裹详细信息
        selected_package_ids = session.get('selected_packages', [])
        if selected_package_ids:
            # 用选中的包裹ID列表从数据库中获取详细信息
            format_strings = ','.join(['%s'] * len(selected_package_ids))
            cur.execute(f"SELECT * FROM packages WHERE tracking_number IN ({format_strings})", tuple(selected_package_ids))
            selected_packages = cur.fetchall()
        else:
            selected_packages = []

        return render_template('fill_order_info.html', selected_packages=selected_packages,
                               addresses=addresses, selected_address=selected_address)






        #  return render_template('fill_order_info.html', selected_packages=session.get('selected_packages', []),
        #                       addresses=addresses, selected_address=selected_address)


@app.route('/view_order_packages/<int:order_id>')
def view_order_packages(order_id):
    # 查询与订单关联的包裹信息
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM packages WHERE order_id = %s", (order_id,))
    order_packages = cur.fetchall()
    return render_template('view_order_packages.html', order_packages=order_packages)

@app.route('/my_orders')
def my_orders():
    # 检查用户是否已登录
    if 'username' not in session:
        return redirect(url_for('login'))  # 如果用户未登录，则重定向到登录页面

    # 获取当前登录用户的用户名
    username = session['username']

    # 连接到数据库
    cur = mysql.connection.cursor()

    # 执行查询当前用户订单数据的SQL语句，按创建时间降序排列
    cur.execute("SELECT * FROM orders WHERE user_id = (SELECT id FROM users WHERE username = %s) ORDER BY created_at DESC", (username,))
    orders = cur.fetchall()  # 获取查询结果

    # 关闭数据库连接
    cur.close()

    # 将订单数据传递给模板进行渲染
    return render_template('my_orders.html', orders=orders)


@app.route('/pending_review_orders')
def pending_review_orders():
    # 检查用户是否已登录
    if 'username' not in session:
        return redirect(url_for('login'))  # 如果用户未登录，则重定向到登录页面

    # 获取当前登录用户的用户名
    username = session['username']

    # 连接到数据库
    cur = mysql.connection.cursor()

    # 执行查询当前用户待处理订单数据的SQL语句，按创建时间降序排列
    cur.execute("""
        SELECT * FROM orders 
        WHERE user_id = (SELECT id FROM users WHERE username = %s) 
        AND order_status = %s 
        ORDER BY created_at DESC
    """, (username, '待处理'))
    orders = cur.fetchall()  # 获取查询结果

    # 关闭数据库连接
    cur.close()

    # 将订单数据传递给模板进行渲染
    return render_template('pending_review_orders.html', orders=orders)




#查看待支付订单
@app.route('/pending_orders')
def pending_orders():
    # 检查用户是否已登录
    if 'username' not in session:
        return redirect(url_for('login'))  # 如果用户未登录，则重定向到登录页面

        # 获取当前登录用户的会员ID
    username = session['username']
    cur = mysql.connection.cursor()
    cur.execute("SELECT member_id FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    member_id = user['member_id']

    # 连接到数据库
    cur = mysql.connection.cursor()

    # 执行查询当前用户待处理订单数据的SQL语句，按创建时间降序排列
    cur.execute("""
               SELECT * FROM orders 
               WHERE user_id = (SELECT id FROM users WHERE username = %s) 
               AND order_status = %s 
               ORDER BY created_at DESC
           """, (username, '待支付'))
    orders = cur.fetchall()  # 获取查询结果

    # 关闭数据库连接
    cur.close()

    # 将订单数据传递给模板进行渲染
    return render_template('pending_orders.html', orders=orders)



from datetime import datetime

@app.route('/pay_order/<int:order_id>', methods=['POST'])
def pay_order(order_id):
    # 检查用户是否登录
    if 'username' not in session:
        return redirect(url_for('login'))

    # 获取当前登录用户的用户名和会员ID
    username = session['username']
    cur = mysql.connection.cursor()
    cur.execute("SELECT member_id FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    member_id = user['member_id']

    # 检查订单是否属于当前用户且状态为待支付
    cur.execute("SELECT * FROM orders WHERE id = %s AND member_id = %s AND order_status = '待支付'", (order_id, member_id))
    order = cur.fetchone()

    # 如果订单不存在或者订单不属于当前用户或者订单状态不是待支付，则返回错误页面
    if not order:
        return "错误：订单不存在或者订单不属于当前用户或者订单状态不是待支付"

    # 获取订单金额
    payment_amount = order['payment_amount']

    # 查询用户钱包余额
    cur.execute("SELECT balance FROM wallets WHERE member_id = %s", (member_id,))
    wallet = cur.fetchone()
    balance = wallet['balance']

    # 检查余额是否足够支付订单
    if balance < payment_amount:
        return "错误：钱包余额不足"

    # 在这里编写支付订单的逻辑
    # 例如，减少钱包余额，并更新订单状态为已支付
    new_balance = balance - payment_amount
    cur.execute("UPDATE wallets SET balance = %s WHERE member_id = %s", (new_balance, member_id))
    cur.execute("UPDATE orders SET order_status = '已支付' WHERE id = %s", (order_id,))

    # 插入交易日期时间数据
    transaction_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cur.execute("UPDATE orders SET transaction_datetime = %s WHERE id = %s", (transaction_datetime, order_id))

    # 提交事务并关闭游标
    mysql.connection.commit()
    cur.close()

    # 返回一个简单的成功页面，您需要根据实际情况进行修改
    return "订单支付成功！"

#查看待发货订单
@app.route('/awaiting_shipment_orders')
def awaiting_shipment_orders():
    # 检查用户是否已登录
    if 'username' not in session:
        return redirect(url_for('login'))  # 如果用户未登录，则重定向到登录页面

    # 获取当前登录用户的用户名
    username = session['username']

    # 连接到数据库
    cur = mysql.connection.cursor()

    # 执行查询当前用户待处理订单数据的SQL语句，按创建时间降序排列
    cur.execute("""
               SELECT * FROM orders 
               WHERE user_id = (SELECT id FROM users WHERE username = %s) 
               AND order_status = %s 
               ORDER BY created_at DESC
           """, (username, '待发货'))
    orders = cur.fetchall()  # 获取查询结果

    # 关闭数据库连接
    cur.close()

    # 将订单数据传递给模板进行渲染
    return render_template('awaiting_shipment_orders.html', orders=orders)


#查看已发货订单
@app.route('/shipped_orders')
def shipped_orders():
    # 检查用户是否已登录
    if 'username' not in session:
        return redirect(url_for('login'))  # 如果用户未登录，则重定向到登录页面

    # 获取当前登录用户的用户名
    username = session['username']

    # 连接到数据库
    cur = mysql.connection.cursor()

    # 执行查询当前用户待处理订单数据的SQL语句，按创建时间降序排列
    cur.execute("""
            SELECT * FROM orders 
            WHERE user_id = (SELECT id FROM users WHERE username = %s) 
            AND order_status = %s 
            ORDER BY created_at DESC
        """, (username, '已发货'))
    orders = cur.fetchall()  # 获取查询结果

    # 关闭数据库连接
    cur.close()

    # 将订单数据传递给模板进行渲染
    return render_template('shipped_orders.html', orders=orders)


#查看已签收订单
@app.route('/deliver_orders')
def deliver_orders():
    # 检查用户是否已登录
    if 'username' not in session:
        return redirect(url_for('login'))  # 如果用户未登录，则重定向到登录页面

        # 获取当前登录用户的会员ID
    username = session['username']
    cur = mysql.connection.cursor()
    cur.execute("SELECT member_id FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    member_id = user['member_id']

    # 连接到数据库
    cur = mysql.connection.cursor()

    # 执行查询当前用户待处理订单数据的SQL语句，按创建时间降序排列
    cur.execute("""
               SELECT * FROM orders 
               WHERE user_id = (SELECT id FROM users WHERE username = %s) 
               AND order_status = %s 
               ORDER BY created_at DESC
           """, (username, '已签收'))
    orders = cur.fetchall()  # 获取查询结果

    # 关闭数据库连接
    cur.close()

    # 将订单数据传递给模板进行渲染
    return render_template('deliver_orders.html', orders=orders)


# 上传图片的路由
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # 获取上传的文件
        image = request.files['image']
        if image:
            # 生成唯一文件名
            filename = generate_unique_filename(image.filename)
            # 保存文件到指定路径
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return '上传成功'
        else:
            return '未选择文件'
    return render_template('upload_form.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    # 返回存储图片的文件夹中的图片文件
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# 钱包管理路由
@app.route('/wallet')
def wallet():
    # 检查用户是否登录
    if 'username' not in session:
        return redirect(url_for('login'))

    # 获取当前登录用户的用户名
    username = session['username']

    # 查询当前用户的会员ID
    cur = mysql.connection.cursor()
    cur.execute("SELECT member_id FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    member_id = user['member_id']

    # 查询当前用户的钱包余额
    cur.execute("SELECT balance FROM wallets WHERE member_id = %s", (member_id,))
    wallet = cur.fetchone()
    balance = wallet['balance']

    # 关闭数据库连接
    cur.close()

    # 渲染钱包管理页面，并传递钱包余额数据
    return render_template('wallet.html', balance=balance)


@app.route('/track', methods=['GET', 'POST'])
def track():
    if request.method == 'POST':
        documentCode = request.form['documentCode']
        url = f"http://120.77.221.225:8082/selectTrack.htm?documentCode={documentCode}"

        try:
            response = requests.get(url)
            data = response.json()

            # 打印相关信息
            print("Received documentCode:", documentCode)

            # 从数据中提取所有 'track_content' 字段
            all_track_content = [item['track_content'] for item in data[0]['data'][0]['trackDetails']]

            # 渲染模板并传递所有跟踪内容数据
            return render_template('track.html', all_track_content=all_track_content)
        except Exception as e:
            # 处理异常情况，例如请求失败或数据格式不正确
            error_message = f"Error occurred: {str(e)}"
            print(error_message)
            return render_template('error.html', error_message=error_message)

    # 如果是 GET 请求，则渲染带有输入表单的页面
    return render_template('track.html')

# 配置API的基础URL和授权编码
API_URL = "http://www.yd-wl.com/api/ApiTracking.ashx"
API_CODE = "a8143a28a1d6067e"

@app.route('/track_yundi', methods=['GET', 'POST'])
def track_yundi():
    tracking_info = None
    if request.method == 'POST':
        tracking_no = request.form['tracking_no']
        response = requests.get(API_URL, params={'trakingno': tracking_no, 'apicode': API_CODE})
        if response.status_code == 200:
            data = response.json()
            if data.get("res") == 1:
                tracking_info = data.get("data")
            else:
                tracking_info = "查询的单号不存在或错误"
        else:
            tracking_info = "API 请求失败"
    return render_template('track_yundi.html', tracking_info=tracking_info)


@app.route('/other')
def other():
    return render_template('other.html')


@app.route('/ase')
def ase():
    return render_template('ase.html')
@app.route('/ase1')
def ase1():
    return render_template('ase1.html')



#if __name__ == '__main__':
  #  app.run(debug=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)