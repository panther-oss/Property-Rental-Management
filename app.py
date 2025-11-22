from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'manideep',  # Change this
    'database': 'propertyrental'
}

def get_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# ==================== PROPERTY ROUTES ====================
@app.route('/api/properties', methods=['GET'])
def get_properties():
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.*, o.Name as Owner_Name 
        FROM property p 
        LEFT JOIN owner o ON p.Owner_ID = o.Owner_ID
    """)
    properties = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(properties)

@app.route('/api/properties/<int:id>', methods=['GET'])
def get_property(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM property WHERE Property_ID = %s", (id,))
    property = cursor.fetchone()
    cursor.close()
    conn.close()
    return jsonify(property)

@app.route('/api/properties', methods=['POST'])
def create_property():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """INSERT INTO property (Address, Size_Sqft, Property_Type, Booking_Status, 
               Property_Cost, City, Furnished, Owner_ID) 
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
    
    values = (data['Address'], data['Size_Sqft'], data['Property_Type'], 
              data['Booking_Status'], data['Property_Cost'], data['City'], 
              data['Furnished'], data['Owner_ID'])
    
    cursor.execute(query, values)
    conn.commit()
    property_id = cursor.lastrowid
    cursor.close()
    conn.close()
    
    return jsonify({'id': property_id, 'message': 'Property created successfully'}), 201

@app.route('/api/properties/<int:id>', methods=['PUT'])
def update_property(id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """UPDATE property SET Address=%s, Size_Sqft=%s, Property_Type=%s, 
               Booking_Status=%s, Property_Cost=%s, City=%s, Furnished=%s, Owner_ID=%s 
               WHERE Property_ID=%s"""
    
    values = (data['Address'], data['Size_Sqft'], data['Property_Type'], 
              data['Booking_Status'], data['Property_Cost'], data['City'], 
              data['Furnished'], data['Owner_ID'], id)
    
    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({'message': 'Property updated successfully'})

@app.route('/api/properties/<int:id>', methods=['DELETE'])
def delete_property(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM property WHERE Property_ID = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Property deleted successfully'})

# ==================== TENANT ROUTES ====================
@app.route('/api/tenants', methods=['GET'])
def get_tenants():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tenant")
    tenants = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(tenants)

@app.route('/api/tenants', methods=['POST'])
def create_tenant():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "INSERT INTO tenant (Name, Phone, Email, Income) VALUES (%s, %s, %s, %s)"
    values = (data['Name'], data['Phone'], data['Email'], data['Income'])
    
    cursor.execute(query, values)
    conn.commit()
    tenant_id = cursor.lastrowid
    cursor.close()
    conn.close()
    
    return jsonify({'id': tenant_id, 'message': 'Tenant created successfully'}), 201

@app.route('/api/tenants/<int:id>', methods=['PUT'])
def update_tenant(id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "UPDATE tenant SET Name=%s, Phone=%s, Email=%s, Income=%s WHERE Tenant_ID=%s"
    values = (data['Name'], data['Phone'], data['Email'], data['Income'], id)
    
    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({'message': 'Tenant updated successfully'})

@app.route('/api/tenants/<int:id>', methods=['DELETE'])
def delete_tenant(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tenant WHERE Tenant_ID = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Tenant deleted successfully'})

# ==================== OWNER ROUTES ====================
@app.route('/api/owners', methods=['GET'])
def get_owners():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM owner")
    owners = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(owners)

@app.route('/api/owners', methods=['POST'])
def create_owner():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "INSERT INTO owner (Name, Phone, Email, Bank_Account) VALUES (%s, %s, %s, %s)"
    values = (data['Name'], data['Phone'], data['Email'], data['Bank_Account'])
    
    cursor.execute(query, values)
    conn.commit()
    owner_id = cursor.lastrowid
    cursor.close()
    conn.close()
    
    return jsonify({'id': owner_id, 'message': 'Owner created successfully'}), 201

@app.route('/api/owners/<int:id>', methods=['PUT'])
def update_owner(id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "UPDATE owner SET Name=%s, Phone=%s, Email=%s, Bank_Account=%s WHERE Owner_ID=%s"
    values = (data['Name'], data['Phone'], data['Email'], data['Bank_Account'], id)
    
    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({'message': 'Owner updated successfully'})

@app.route('/api/owners/<int:id>', methods=['DELETE'])
def delete_owner(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM owner WHERE Owner_ID = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Owner deleted successfully'})

# ==================== LEASE ROUTES ====================
@app.route('/api/leases', methods=['GET'])
def get_leases():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT l.*, t.Name as Tenant_Name, p.Address as Property_Address
        FROM lease l
        LEFT JOIN tenant t ON l.Tenant_ID = t.Tenant_ID
        LEFT JOIN property p ON l.Property_ID = p.Property_ID
    """)
    leases = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(leases)

@app.route('/api/leases', methods=['POST'])
def create_lease():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """INSERT INTO lease (Start_Date, End_Date, Monthly_Rent, Security_Deposit, 
               Property_ID, Tenant_ID) VALUES (%s, %s, %s, %s, %s, %s)"""
    
    values = (data['Start_Date'], data['End_Date'], data['Monthly_Rent'], 
              data['Security_Deposit'], data['Property_ID'], data['Tenant_ID'])
    
    cursor.execute(query, values)
    conn.commit()
    lease_id = cursor.lastrowid
    cursor.close()
    conn.close()
    
    return jsonify({'id': lease_id, 'message': 'Lease created successfully'}), 201

@app.route('/api/leases/<int:id>', methods=['PUT'])
def update_lease(id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """UPDATE lease SET Start_Date=%s, End_Date=%s, Monthly_Rent=%s, 
               Security_Deposit=%s, Property_ID=%s, Tenant_ID=%s WHERE Lease_ID=%s"""
    
    values = (data['Start_Date'], data['End_Date'], data['Monthly_Rent'], 
              data['Security_Deposit'], data['Property_ID'], data['Tenant_ID'], id)
    
    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({'message': 'Lease updated successfully'})

@app.route('/api/leases/<int:id>', methods=['DELETE'])
def delete_lease(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM lease WHERE Lease_ID = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Lease deleted successfully'})

# ==================== PAYMENT ROUTES ====================
@app.route('/api/payments', methods=['GET'])
def get_payments():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.*, l.Property_ID, t.Name as Tenant_Name
        FROM payment p
        LEFT JOIN lease l ON p.Lease_ID = l.Lease_ID
        LEFT JOIN tenant t ON l.Tenant_ID = t.Tenant_ID
    """)
    payments = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(payments)

@app.route('/api/payments', methods=['POST'])
def create_payment():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """INSERT INTO payment (Payment_Date, Amount, Mode_of_Payment, Status, Lease_ID) 
               VALUES (%s, %s, %s, %s, %s)"""
    
    values = (data['Payment_Date'], data['Amount'], data['Mode_of_Payment'], 
              data['Status'], data['Lease_ID'])
    
    try:
        cursor.execute(query, values)
        conn.commit()
        payment_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return jsonify({'id': payment_id, 'message': 'Payment created successfully'}), 201
    except Error as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/payments/<int:id>', methods=['DELETE'])
def delete_payment(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM payment WHERE Payment_ID = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Payment deleted successfully'})

# ==================== MAINTENANCE ROUTES ====================
@app.route('/api/maintenance', methods=['GET'])
def get_maintenance():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT m.*, p.Address as Property_Address
        FROM maintenance m
        LEFT JOIN property p ON m.Property_ID = p.Property_ID
    """)
    maintenance = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(maintenance)

@app.route('/api/maintenance', methods=['POST'])
def create_maintenance():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """INSERT INTO maintenance (Maintenance_Date, Maintenance_Type, Cost, Status, Property_ID) 
               VALUES (%s, %s, %s, %s, %s)"""
    
    values = (data['Maintenance_Date'], data['Maintenance_Type'], data['Cost'], 
              data['Status'], data['Property_ID'])
    
    cursor.execute(query, values)
    conn.commit()
    maintenance_id = cursor.lastrowid
    cursor.close()
    conn.close()
    
    return jsonify({'id': maintenance_id, 'message': 'Maintenance record created successfully'}), 201

@app.route('/api/maintenance/<int:id>', methods=['PUT'])
def update_maintenance(id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """UPDATE maintenance SET Maintenance_Date=%s, Maintenance_Type=%s, Cost=%s, 
               Status=%s, Property_ID=%s WHERE Maintenance_ID=%s"""
    
    values = (data['Maintenance_Date'], data['Maintenance_Type'], data['Cost'], 
              data['Status'], data['Property_ID'], id)
    
    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({'message': 'Maintenance record updated successfully'})

@app.route('/api/maintenance/<int:id>', methods=['DELETE'])
def delete_maintenance(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM maintenance WHERE Maintenance_ID = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Maintenance record deleted successfully'})

# ==================== COMPLAINT ROUTES ====================
@app.route('/api/complaints', methods=['GET'])
def get_complaints():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT c.*, t.Name as Tenant_Name, p.Address as Property_Address
        FROM complaint c
        LEFT JOIN tenant t ON c.Tenant_ID = t.Tenant_ID
        LEFT JOIN property p ON c.Property_ID = p.Property_ID
    """)
    complaints = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(complaints)

@app.route('/api/complaints', methods=['POST'])
def create_complaint():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """INSERT INTO complaint (Complaint_Date, Status, Tenant_ID, Property_ID) 
               VALUES (%s, %s, %s, %s)"""
    
    values = (data['Complaint_Date'], data['Status'], data['Tenant_ID'], data['Property_ID'])
    
    cursor.execute(query, values)
    conn.commit()
    complaint_id = cursor.lastrowid
    cursor.close()
    conn.close()
    
    return jsonify({'id': complaint_id, 'message': 'Complaint created successfully'}), 201

@app.route('/api/complaints/<int:id>', methods=['PUT'])
def update_complaint(id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "UPDATE complaint SET Status=%s WHERE Complaint_ID=%s"
    values = (data['Status'], id)
    
    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({'message': 'Complaint updated successfully'})

@app.route('/api/complaints/<int:id>', methods=['DELETE'])
def delete_complaint(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM complaint WHERE Complaint_ID = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Complaint deleted successfully'})

# ==================== DASHBOARD/STATS ROUTE ====================
@app.route('/api/dashboard', methods=['GET'])
def get_dashboard_stats():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    stats = {}
    
    cursor.execute("SELECT COUNT(*) as count FROM property")
    stats['total_properties'] = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM property WHERE Booking_Status = 'Rented'")
    stats['rented_properties'] = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM tenant")
    stats['total_tenants'] = cursor.fetchone()['count']
    
    cursor.execute("SELECT SUM(Amount) as total FROM payment WHERE Status = 'Completed'")
    result = cursor.fetchone()
    stats['total_revenue'] = result['total'] if result['total'] else 0
    
    cursor.execute("SELECT COUNT(*) as count FROM maintenance WHERE Status = 'Pending'")
    stats['pending_maintenance'] = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM complaint WHERE Status = 'Under Review'")
    stats['pending_complaints'] = cursor.fetchone()['count']
    
    cursor.close()
    conn.close()
    
    return jsonify(stats)

# ==================== STORED PROCEDURES ROUTES ====================

@app.route('/api/reports/property-revenue/<int:property_id>', methods=['GET'])
def get_property_revenue(property_id):
    """Call GetPropertyRevenue stored procedure"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.callproc('GetPropertyRevenue', [property_id])
    
    # Fetch results from the stored procedure
    results = []
    for result in cursor.stored_results():
        results = result.fetchall()
    
    cursor.close()
    conn.close()
    
    return jsonify(results[0] if results else {})

@app.route('/api/reports/tenant-payment-history/<int:tenant_id>', methods=['GET'])
def get_tenant_payment_history(tenant_id):
    """Call GetTenantPaymentHistory stored procedure"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.callproc('GetTenantPaymentHistory', [tenant_id])
    
    results = []
    for result in cursor.stored_results():
        results = result.fetchall()
    
    cursor.close()
    conn.close()
    
    return jsonify(results)

@app.route('/api/reports/monthly-rent/<int:month>/<int:year>', methods=['GET'])
def get_monthly_rent_report(month, year):
    """Call GetMonthlyRentReport stored procedure"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.callproc('GetMonthlyRentReport', [month, year])
    
    results = []
    for result in cursor.stored_results():
        results = result.fetchall()
    
    cursor.close()
    conn.close()
    
    return jsonify(results)

@app.route('/api/reports/maintenance-cost/<int:property_id>', methods=['GET'])
def get_maintenance_cost(property_id):
    """Call GetMaintenanceCostByProperty stored procedure"""
    start_date = request.args.get('start_date', '2025-01-01')
    end_date = request.args.get('end_date', '2025-12-31')
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.callproc('GetMaintenanceCostByProperty', [property_id, start_date, end_date])
    
    results = []
    for result in cursor.stored_results():
        results = result.fetchall()
    
    cursor.close()
    conn.close()
    
    return jsonify(results[0] if results else {})

@app.route('/api/complaints/<int:complaint_id>/update-status', methods=['POST'])
def update_complaint_status_proc(complaint_id):
    """Call UpdateComplaintStatus stored procedure"""
    data = request.json
    new_status = data.get('status')
    action = data.get('action', f'Status updated to {new_status}')
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.callproc('UpdateComplaintStatus', [complaint_id, new_status, action])
    
    results = []
    for result in cursor.stored_results():
        results = result.fetchall()
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify(results[0] if results else {})

# ==================== FUNCTIONS ROUTES ====================

@app.route('/api/functions/total-rent/<int:lease_id>', methods=['GET'])
def calculate_total_rent(lease_id):
    """Call CalculateTotalRent function"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT CalculateTotalRent(%s) as total_rent", (lease_id,))
    result = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    return jsonify(result)

@app.route('/api/functions/pending-payments/<int:tenant_id>', methods=['GET'])
def has_pending_payments(tenant_id):
    """Call HasPendingPayments function"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT HasPendingPayments(%s) as has_pending", (tenant_id,))
    result = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    return jsonify(result)

@app.route('/api/functions/occupancy-rate/<int:owner_id>', methods=['GET'])
def get_occupancy_rate(owner_id):
    """Call GetPropertyOccupancyRate function"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT GetPropertyOccupancyRate(%s) as occupancy_rate", (owner_id,))
    result = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    return jsonify(result)

@app.route('/api/functions/outstanding-balance/<int:tenant_id>', methods=['GET'])
def get_outstanding_balance(tenant_id):
    """Call GetTenantOutstandingBalance function"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT GetTenantOutstandingBalance(%s) as outstanding_balance", (tenant_id,))
    result = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    return jsonify(result)

@app.route('/api/functions/avg-maintenance-cost/<property_type>', methods=['GET'])
def get_avg_maintenance_cost(property_type):
    """Call GetAvgMaintenanceCostByType function"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT GetAvgMaintenanceCostByType(%s) as avg_cost", (property_type,))
    result = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    return jsonify(result)

@app.route('/api/functions/property-available/<int:property_id>', methods=['GET'])
def is_property_available(property_id):
    """Call IsPropertyAvailable function"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT IsPropertyAvailable(%s) as is_available", (property_id,))
    result = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    return jsonify(result)

# ==================== MAIN ROUTES ====================
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reports')
def reports():
    return render_template('reports.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)