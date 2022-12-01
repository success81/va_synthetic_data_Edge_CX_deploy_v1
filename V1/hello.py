from flask import Flask, render_template, request
import pandas as pd
import pickle
my_punct = {'=', '-', '/', '{', '#', '"', '(', '@', '$', '`', ',', ')', '+', '?', '.', '|', '}', '[', '_', '^', ';', '%', '&', '<', '>', ':', '\\', '~', '*', '!', ']',"1","2","3","4","5","6","7","8","9","0"}
clf = pickle.load(open('gradient_synth_data','rb'))
count_vect = pickle.load(open('gradient_countvector','rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/predict', methods=['GET', 'POST'])
def home():
    def string_break(input):
        blank_string = ""
        for x in input:
            if x not in my_punct:
                blank_string += x.lower()
        output = blank_string.split()
        return output

    def va_prediction(comment):
      big_comment = comment.lower()
      my_comment = pd.Series(big_comment)
      big_predict = clf.predict(count_vect.transform(my_comment))
      check_comment = string_break(big_comment)
      token_input = string_break(comment)
      a = big_predict.tolist()
      final_prediction = a[0]

      staff = ["staff","desk","doctors","nurse","doctor"]
      facility = ["bathrooms", "bathroom", "dirty","clean","filthy","sanitary"]
      mental_health = ["suicide", "mental", "suicidal"]

      positive_response = "We are so glad that you had an amazing experience today.It was our pleasure! Thank you for your service"
      negative_response = "I'm sorry your experience wasn't the best today. Feel free to contact the patient advocate team at 555-555-5555. They will be able to address any unresolved issues."

      positive_staff = "We are glad to hear that you had a great experience with our staff. We pride ourselves on taking care of veterans. Thank you for your service."
      negative_staff = "We are so sorry to hear about your negative staff experience today. Please contact our patient advocate team at 555-555-5555 so we can look into this issue."

      facility_negative= "We are so sorry to hear that our facilities didn't meet your expectations. Please contact our facilities team at 555-555-5555 and let them know your issues. Thank you for your service."
      facility_positive= "Thank you so much. We pride ourselves on the cleanliness of our building. We will pass your nice words to our facilities team."

      mental_health_negative = "We apologize for your negative experience today with our mental health department. Your well-being is very important to us. If you're feeling suicidal please contact 911 or the Veteran Suicide Line by dialing 988."

      #Counters
      staff_counter = 0
      facility_counter = 0
      mental_health_counter = 0
      negative_counter = 0
      positive_counter = 0
      if final_prediction == "negative":
        negative_counter = 1
      if final_prediction == "positive":
        positive_counter = 1
      
      for x in check_comment:
        if x in staff:
          staff_counter += 1
        if x in facility:
          facility_counter += 1
        if x in mental_health:
          mental_health_counter += 1
      
      if mental_health_counter > 0 and negative_counter == 1:
        return mental_health_negative
      
      if staff_counter > 0 and negative_counter == 1:
        return negative_staff
      
      if staff_counter > 0 and positive_counter == 1:
        return positive_staff
      
      if facility_counter > 0 and positive_counter == 1:
        return facility_positive
      
      if facility_counter > 0 and negative_counter == 1:
        return facility_negative
      
      if negative_counter == 1:
        return negative_response
      
      if positive_counter == 1:
        return positive_response
            
    transfer = va_prediction(request.form['k'])

    


    return render_template('after.html', data = transfer)
if __name__ == "__main__":
    app.run(debug=True)
