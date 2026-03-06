import pandas as pd
import os

class IdentityAnalyzer:
    def __init__(self, data_file='data/identities.csv'):
        self.data_file = data_file
        self.df = pd.DataFrame()
        self.load_data()

    def load_data(self):
        """Loads data from the CSV file."""
        if os.path.exists(self.data_file):
            try:
                self.df = pd.read_csv(self.data_file)
            except Exception as e:
                print(f"Error loading data: {e}")
                self.df = pd.DataFrame(columns=['Name', 'Email', 'Phone', 'Username', 'Platform', 'PasswordStrength'])
        else:
            self.df = pd.DataFrame(columns=['Name', 'Email', 'Phone', 'Username', 'Platform', 'PasswordStrength'])
            self.save_data()

    def save_data(self):
        """Saves the current DataFrame to the CSV file."""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        self.df.to_csv(self.data_file, index=False)

    def add_entry(self, entry):
        """Adds a single manual entry."""
        new_entry = pd.DataFrame([entry])
        self.df = pd.concat([self.df, new_entry], ignore_index=True)
        self.save_data()
        return True

    def process_csv(self, file_path):
        """Merges an uploaded CSV with the current dataset."""
        try:
            uploaded_df = pd.read_csv(file_path)
            # Ensure required columns exist
            required_cols = ['Name', 'Email', 'Phone', 'Username', 'Platform', 'PasswordStrength']
            if not all(col in uploaded_df.columns for col in required_cols):
                return False, "Missing required columns in CSV."
            
            self.df = pd.concat([self.df, uploaded_df], ignore_index=True).drop_duplicates()
            self.save_data()
            return True, "Data uploaded successfully."
        except Exception as e:
            return False, str(e)

    def analyze_risks(self):
        """Performs the core risk analysis."""
        if self.df.empty:
            return {
                'total_platforms': 0,
                'risk_level': 'Low',
                'risk_score': 0,
                'fragmentation_score': 0,
                'duplication_ratio': 0,
                'recommendations': []
            }

        total_platforms = len(self.df)
        unique_emails = self.df['Email'].nunique()
        unique_phones = self.df['Phone'].nunique()
        unique_usernames = self.df['Username'].nunique()

        # Duplication Ratio: 1 - (Unique Attributes / Total Platforms)
        # Higher is worse (more reused attributes across platforms)
        total_attributes = (total_platforms * 3) # Email, Phone, Username per platform
        unique_total = unique_emails + unique_phones + unique_usernames
        duplication_ratio = 1 - (unique_total / total_attributes) if total_attributes > 0 else 0

        # Risk Calculation Logic
        risk_score = 0
        
        # 1. Surface Area Risk (Total Platforms)
        if total_platforms > 15:
            risk_score += 30
        elif total_platforms > 5:
            risk_score += 15
        else:
            risk_score += 5

        # 2. Fragmentation / Re-use Risk
        # High re-use of same email/phone is risky if compromised.
        # Check for email reuse
        email_counts = self.df['Email'].value_counts()
        if (email_counts > 1).any():
             risk_score += 25 # Significant risk if one email is key to many services

        # Check for username reuse (easier to track across web)
        username_counts = self.df['Username'].value_counts()
        if (username_counts > 1).any():
            risk_score += 15

        # 3. Password Strength Analysis (Simulation)
        weak_passwords = self.df[self.df['PasswordStrength'].str.lower() == 'weak'].shape[0]
        risk_score += (weak_passwords * 5) # 5 points per weak password usage

        # Cap score at 100
        risk_score = min(risk_score, 100)

        # Determine Level
        if risk_score >= 70:
            risk_level = "High"
        elif risk_score >= 40:
            risk_level = "Medium"
        else:
            risk_level = "Low"

        # Recommendations
        recommendations = []
        if risk_level == "High":
            recommendations.append("Immediate Action: Enable 2FA on all accounts sharing the main email.")
            recommendations.append("Reduce digital footprint: Delete unused accounts.")
        if (email_counts > 1).any():
             recommendations.append("Warning: High email reuse detected. If your primary email is compromised, multiple accounts are at risk.")
        if weak_passwords > 0:
            recommendations.append(f"Security Alert: {weak_passwords} accounts use weak passwords. Update immediately.")
        if total_platforms > 20:
             recommendations.append("High Fragmentation: Your identity is spread across too many services. Consider using a password manager and auditing accounts.")

        return {
            'total_platforms': total_platforms,
            'risk_level': risk_level,
            'risk_score': round(risk_score, 2),
            'fragmentation_score': round(duplication_ratio * 100, 2),
            'duplication_ratio': round(duplication_ratio, 2),
            'recommendations': recommendations
        }

    def get_dashboard_data(self):
        """Returns data ready for charts."""
        if self.df.empty:
            return {}

        # 1. Platform Distribution (Top 5)
        platform_counts = self.df['Platform'].value_counts().head(5).to_dict()
        
        # 2. Password Strength Distribution
        password_strength = self.df['PasswordStrength'].value_counts().to_dict()

        return {
            'platforms': list(platform_counts.keys()),
            'platform_counts': list(platform_counts.values()),
            'password_labels': list(password_strength.keys()),
            'password_values': list(password_strength.values())
        }
