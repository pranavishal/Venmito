from flask import Blueprint, request, jsonify
from sqlalchemy import create_engine, text
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../storage/venmito.db"))
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"
engine = create_engine(DATABASE_URL)

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
chatbot_blueprint = Blueprint('chatbot', __name__)

def get_database_summary():
    """Get comprehensive summary of all data"""
    try:
        with engine.connect() as conn:
            summary = {}
            
            # Top Spending Customers
            top_spenders = conn.execute(text("""
                SELECT 
                    p.firstName || ' ' || p.surname as customer_name,
                    p.id as customer_id,
                    p.email,
                    COUNT(t.id) as transaction_count,
                    SUM(t.total_price) as total_spent,
                    AVG(t.total_price) as avg_transaction,
                    MAX(t.total_price) as largest_transaction
                FROM people p
                JOIN transactions t ON p.id = t.customer_id
                GROUP BY p.id
                ORDER BY total_spent DESC
                LIMIT 10
            """)).fetchall()
            
            summary['top_spenders'] = [{
                'name': row[0],
                'customer_id': row[1],
                'email': row[2],
                'transaction_count': row[3],
                'total_spent': float(row[4]),
                'avg_transaction': float(row[5]),
                'largest_transaction': float(row[6])
            } for row in top_spenders]

            # Most Frequent Transactors
            frequent_buyers = conn.execute(text("""
                SELECT 
                    p.firstName || ' ' || p.surname as customer_name,
                    p.id as customer_id,
                    p.email,
                    COUNT(t.id) as transaction_count,
                    SUM(t.total_price) as total_spent,
                    COUNT(DISTINCT t.store) as unique_stores
                FROM people p
                JOIN transactions t ON p.id = t.customer_id
                GROUP BY p.id
                ORDER BY transaction_count DESC
                LIMIT 10
            """)).fetchall()
            
            summary['frequent_buyers'] = [{
                'name': row[0],
                'customer_id': row[1],
                'email': row[2],
                'transaction_count': row[3],
                'total_spent': float(row[4]),
                'unique_stores': row[5]
            } for row in frequent_buyers]

            # Promotion Response Analysis
            promotion_stats = conn.execute(text("""
                SELECT 
                    promotion,
                    COUNT(*) as total_sent,
                    SUM(CASE WHEN responded = 'Yes' THEN 1 ELSE 0 END) as yes_responses,
                    ROUND(CAST(SUM(CASE WHEN responded = 'Yes' THEN 1 ELSE 0 END) AS FLOAT) / 
                          COUNT(*) * 100, 2) as response_rate
                FROM promotions
                GROUP BY promotion
                ORDER BY response_rate DESC
            """)).fetchall()
            
            summary['promotion_stats'] = [{
                'promotion': row[0],
                'total_sent': row[1],
                'yes_responses': row[2],
                'response_rate': float(row[3])
            } for row in promotion_stats]

            # Best Responding Customers to Promotions
            promotion_champions = conn.execute(text("""
                SELECT 
                    p.firstName || ' ' || p.surname as customer_name,
                    pr.client_email,
                    COUNT(*) as total_promotions_received,
                    SUM(CASE WHEN pr.responded = 'Yes' THEN 1 ELSE 0 END) as promotions_accepted,
                    ROUND(CAST(SUM(CASE WHEN pr.responded = 'Yes' THEN 1 ELSE 0 END) AS FLOAT) / 
                          COUNT(*) * 100, 2) as response_rate
                FROM promotions pr
                JOIN people p ON pr.client_email = p.email
                GROUP BY pr.client_email
                HAVING COUNT(*) >= 3  -- Only include customers with at least 3 promotions
                ORDER BY response_rate DESC
                LIMIT 10
            """)).fetchall()
            
            summary['promotion_champions'] = [{
                'name': row[0],
                'email': row[1],
                'total_promotions': row[2],
                'accepted_promotions': row[3],
                'response_rate': float(row[4])
            } for row in promotion_champions]

            # Promotion and Transaction Correlation
            promo_transaction_correlation = conn.execute(text("""
                WITH customer_stats AS (
                    SELECT 
                        p.email,
                        COUNT(DISTINCT pr.promotion) as promotions_received,
                        SUM(CASE WHEN pr.responded = 'Yes' THEN 1 ELSE 0 END) as promotions_accepted,
                        COUNT(DISTINCT t.id) as transaction_count,
                        SUM(t.total_price) as total_spent
                    FROM people p
                    LEFT JOIN promotions pr ON p.email = pr.client_email
                    LEFT JOIN transactions t ON p.id = t.customer_id
                    GROUP BY p.email
                )
                SELECT 
                    AVG(promotions_received) as avg_promotions_per_customer,
                    AVG(promotions_accepted) as avg_accepted_promotions,
                    AVG(CASE WHEN promotions_accepted > 0 
                        THEN transaction_count ELSE 0 END) as avg_transactions_after_promotion,
                    AVG(CASE WHEN promotions_accepted > 0 
                        THEN total_spent ELSE 0 END) as avg_spending_after_promotion
                FROM customer_stats
            """)).first()
            
            summary['promotion_impact'] = {
                'avg_promotions_per_customer': float(promo_transaction_correlation[0]),
                'avg_accepted_promotions': float(promo_transaction_correlation[1]),
                'avg_transactions_after_promotion': float(promo_transaction_correlation[2]),
                'avg_spending_after_promotion': float(promo_transaction_correlation[3])
            }

            # Promotion Timing Analysis
            store_performance = conn.execute(text("""
                SELECT 
                    store,
                    COUNT(*) as transaction_count,
                    SUM(total_price) as total_revenue,
                    AVG(total_price) as avg_transaction,
                    COUNT(DISTINCT customer_id) as unique_customers
                FROM transactions 
                GROUP BY store
                ORDER BY total_revenue DESC
            """)).fetchall()
            
            summary['store_performance'] = [{
                'store': row[0],
                'transaction_count': row[1],
                'total_revenue': float(row[2]),
                'avg_transaction': float(row[3]),
                'unique_customers': row[4]
            } for row in store_performance]

            # Top Transfer Senders
            top_senders = conn.execute(text("""
                SELECT 
                    p.firstName || ' ' || p.surname as sender_name,
                    p.id as sender_id,
                    p.email as sender_email,
                    COUNT(*) as transfers_sent,
                    SUM(t.amount) as total_sent,
                    AVG(t.amount) as avg_sent,
                    MAX(t.amount) as largest_sent,
                    COUNT(DISTINCT recipient_id) as unique_recipients
                FROM people p
                JOIN transfers t ON p.id = t.sender_id
                GROUP BY p.id
                ORDER BY total_sent DESC
                LIMIT 10
            """)).fetchall()
            
            summary['top_senders'] = [{
                'name': row[0],
                'id': row[1],
                'email': row[2],
                'transfer_count': row[3],
                'total_sent': float(row[4]),
                'avg_sent': float(row[5]),
                'largest_transfer': float(row[6]),
                'unique_recipients': row[7]
            } for row in top_senders]

            # Top Transfer Recipients
            top_recipients = conn.execute(text("""
                SELECT 
                    p.firstName || ' ' || p.surname as recipient_name,
                    p.id as recipient_id,
                    p.email as recipient_email,
                    COUNT(*) as transfers_received,
                    SUM(t.amount) as total_received,
                    AVG(t.amount) as avg_received,
                    MAX(t.amount) as largest_received,
                    COUNT(DISTINCT sender_id) as unique_senders
                FROM people p
                JOIN transfers t ON p.id = t.recipient_id
                GROUP BY p.id
                ORDER BY total_received DESC
                LIMIT 10
            """)).fetchall()
            
            summary['top_recipients'] = [{
                'name': row[0],
                'id': row[1],
                'email': row[2],
                'transfer_count': row[3],
                'total_received': float(row[4]),
                'avg_received': float(row[5]),
                'largest_transfer': float(row[6]),
                'unique_senders': row[7]
            } for row in top_recipients]

            # Most Active Transfer Pairs
            frequent_pairs = conn.execute(text("""
                SELECT 
                    s.firstName || ' ' || s.surname as sender_name,
                    r.firstName || ' ' || r.surname as recipient_name,
                    COUNT(*) as transfer_count,
                    SUM(t.amount) as total_amount,
                    AVG(t.amount) as avg_amount,
                    MAX(t.amount) as max_amount
                FROM transfers t
                JOIN people s ON t.sender_id = s.id
                JOIN people r ON t.recipient_id = r.id
                GROUP BY t.sender_id, t.recipient_id
                ORDER BY transfer_count DESC
                LIMIT 10
            """)).fetchall()
            
            summary['frequent_pairs'] = [{
                'sender': row[0],
                'recipient': row[1],
                'transfer_count': row[2],
                'total_amount': float(row[3]),
                'avg_amount': float(row[4]),
                'max_amount': float(row[5])
            } for row in frequent_pairs]

            # Transfer Time Analysis
            time_analysis = conn.execute(text("""
                SELECT 
                    strftime('%Y-%m', date) as month,
                    COUNT(*) as transfer_count,
                    SUM(amount) as total_amount,
                    AVG(amount) as avg_amount,
                    COUNT(DISTINCT sender_id) as unique_senders,
                    COUNT(DISTINCT recipient_id) as unique_recipients
                FROM transfers
                GROUP BY strftime('%Y-%m', date)
                ORDER BY month DESC
                LIMIT 12
            """)).fetchall()
            
            summary['transfer_trends'] = [{
                'month': row[0],
                'transfer_count': row[1],
                'total_amount': float(row[2]),
                'avg_amount': float(row[3]),
                'unique_senders': row[4],
                'unique_recipients': row[5]
            } for row in time_analysis]

            # Net Transfer Analysis (Sent - Received)
            net_transfer_analysis = conn.execute(text("""
                WITH transfer_totals AS (
                    SELECT 
                        p.id,
                        p.firstName || ' ' || p.surname as person_name,
                        COALESCE(SUM(CASE WHEN t1.sender_id = p.id THEN t1.amount ELSE 0 END), 0) as total_sent,
                        COALESCE(SUM(CASE WHEN t1.recipient_id = p.id THEN t1.amount ELSE 0 END), 0) as total_received
                    FROM people p
                    LEFT JOIN transfers t1 ON p.id IN (t1.sender_id, t1.recipient_id)
                    GROUP BY p.id
                )
                SELECT 
                    person_name,
                    total_sent,
                    total_received,
                    (total_received - total_sent) as net_transfer
                FROM transfer_totals
                ORDER BY ABS(total_received - total_sent) DESC
                LIMIT 10
            """)).fetchall()
            
            summary['net_transfers'] = [{
                'name': row[0],
                'total_sent': float(row[1]),
                'total_received': float(row[2]),
                'net_transfer': float(row[3])
            } for row in net_transfer_analysis]

            # Overall Transfer Statistics
            transfer_stats = conn.execute(text("""
                SELECT 
                    COUNT(*) as total_transfers,
                    SUM(amount) as total_volume,
                    AVG(amount) as avg_transfer,
                    MIN(amount) as min_transfer,
                    MAX(amount) as max_transfer,
                    COUNT(DISTINCT sender_id) as total_senders,
                    COUNT(DISTINCT recipient_id) as total_recipients
                FROM transfers
            """)).first()
            
            summary['transfer_statistics'] = {
                'total_transfers': transfer_stats[0],
                'total_volume': float(transfer_stats[1]),
                'avg_transfer': float(transfer_stats[2]),
                'min_transfer': float(transfer_stats[3]),
                'max_transfer': float(transfer_stats[4]),
                'unique_senders': transfer_stats[5],
                'unique_recipients': transfer_stats[6]
            }

            return summary
            
    except Exception as e:
        print(f"Error in get_database_summary: {str(e)}")
        return {"error": str(e)}

@chatbot_blueprint.route('/query', methods=['POST'])
def process_query():
    try:
        user_input = request.json.get('query')
        if not user_input:
            return jsonify({"error": "No query provided"}), 400

        db_summary = get_database_summary()
        if "error" in db_summary:
            return jsonify({"error": "Failed to get database summary"}), 500
        
        prompt = f"""You are a financial data and marketing analyst. Based on this detailed database summary:
        {db_summary}
        
        Please analyze the data to answer this question: {user_input}
        
        Consider and include in your analysis:
        - Customer spending patterns and behaviors
        - Promotion effectiveness and response rates
        - Correlation between promotions and customer spending
        - Specific customer examples and statistics
        - Store performance metrics
        - Recommendations for improvement where applicable
        
        Format your response in a clear, professional manner with specific numbers and percentages."""

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert financial and marketing analyst."},
                {"role": "user", "content": prompt}
            ]
        )

        return jsonify({
            "analysis": response.choices[0].message.content
        }), 200

    except Exception as e:
        print(f"Error in process_query: {str(e)}")
        return jsonify({"error": str(e)}), 500