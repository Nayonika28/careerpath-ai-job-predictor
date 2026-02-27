
class CareerModel:
    def __init__(self):
        self.is_trained = True

    def predict_job(self, degree, specialization, cgpa):
        # Already converted to lowercase before calling function
        
        if degree == "btech":
            
            if "cse" in specialization or "computer" in specialization or "csbs" in specialization:
                if cgpa >= 8.5:
                    return "Software Developer"
                elif cgpa >= 7.5:
                    return "Web Developer"
                else:
                    return "Technical Support Engineer"

            elif "ai" in specialization or "artificial intelligence" in specialization or "data science" in specialization:
                if cgpa >= 8.5:
                    return "Data Scientist"
                else:
                    return "ML Engineer Intern"

            elif "ece" in specialization or "electronics" in specialization:
                if cgpa >= 8:
                    return "Embedded Systems Engineer"
                else:
                    return "Network Support Engineer"

        elif degree == "bsc":
            
            if "it" in specialization or "computer" in specialization:
                if cgpa >= 8:
                    return "System Analyst"
                else:
                    return "IT Support Executive"
            
            elif "commerce" in specialization:
                return "Accounts Executive"

        return "Further Skill Development Recommended"

    def predict(self, degree, spec, cgpa):
        # Convert inputs to lowercase for matching
        degree_lower = degree.lower().replace(".", "")
        spec_lower = spec.lower()
        
        # Get primary prediction
        primary_role = self.predict_job(degree_lower, spec_lower, cgpa)
        
        # Generate alternative roles for variety
        alternative_roles = {
            "Software Developer": ["Full Stack Developer", "Backend Engineer"],
            "Web Developer": ["Frontend Developer", "UI/UX Developer"],
            "Data Scientist": ["Data Analyst", "Business Intelligence Analyst"],
            "ML Engineer Intern": ["AI Research Assistant", "Data Science Intern"],
            "Embedded Systems Engineer": ["IoT Developer", "Hardware Engineer"],
            "Network Support Engineer": ["System Administrator", "DevOps Engineer"],
            "System Analyst": ["Business Analyst", "IT Consultant"],
            "IT Support Executive": ["Help Desk Specialist", "Technical Support"],
            "Accounts Executive": ["Financial Analyst", "Accountant"]
        }
        
        # Get alternatives or use generic ones
        alternatives = alternative_roles.get(primary_role, ["General Consultant", "Junior Analyst"])
        
        # Return predictions with confidence scores
        predictions = [
            {"role": primary_role, "confidence": 0.85},
            {"role": alternatives[0], "confidence": 0.70}
        ]
        
        if len(alternatives) > 1:
            predictions.append({"role": alternatives[1], "confidence": 0.55})
        else:
            predictions.append({"role": "Technical Specialist", "confidence": 0.55})
            
        return predictions

    def train(self, df=None):
        # Rule-based model doesn't need training
        self.is_trained = True
        pass
