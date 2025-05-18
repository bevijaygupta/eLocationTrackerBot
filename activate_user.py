import sys
from subscription_manager import activate_plan_after_payment

def main():
    if len(sys.argv) != 4:
        print("Usage: python3 activate_user.py <telegram_id> <plan_type> <subscription_id>")
        return

    try:
        telegram_id = int(sys.argv[1])
        plan_type = sys.argv[2]
        subscription_id = sys.argv[3]

        success = activate_plan_after_payment(telegram_id, plan_type, subscription_id)
        if success:
            print(f"[SUCCESS] Activated {plan_type} plan for Telegram ID {telegram_id}")
        else:
            print(f"[ERROR] Activation failed for Telegram ID {telegram_id} with plan {plan_type}")

    except Exception as e:
        print(f"[EXCEPTION] {e}")

if __name__ == "__main__":
    main()
