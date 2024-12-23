function validateNumberInput(input) {
    input.value = input.value.replace(/[^0-9]/g, '');
}

document.addEventListener('DOMContentLoaded', function () {
    var heightInput = document.getElementById('height');
    var weightInput = document.getElementById('weight');
    var calculateButton = document.getElementById('calculateBMI');
    var resetButton = document.getElementById('resetButton');
    var bmiResult = document.getElementById('bmiResult');
    var rangeResult = document.getElementById('rangeResult');

    calculateButton.addEventListener('click', calculateBMI);
    resetButton.addEventListener('click', resetInputs);

    function calculateBMI() {
        var height = parseFloat(heightInput.value);
        var weight = parseFloat(weightInput.value);

        if (isNaN(height) || isNaN(weight) || height <= 0 || weight <= 0) {
            alert('Please enter valid height and weight values.');
            return;
        }

        var bmi = weight / ((height / 100) * (height / 100));

        bmiResult.textContent = bmi.toFixed(1);

        displayBMIRange(bmi);
    }

    function displayBMIRange(bmi) {
        var rangeElement = document.getElementById('range');

        if (!rangeElement) {
            console.error('Element with id "range" not found.');
            return;
        }
    
        try {
            if (bmi < 18.5) {
                rangeElement.textContent = 'Underweight!';
                rangeElement.style.color = 'rgb(12, 137, 238)';
            } else if (bmi < 25) {
                rangeElement.textContent = 'Healthy!';
                rangeElement.style.color = 'rgb(0, 137, 0)';
            } else if (bmi < 30) {
                rangeElement.textContent = 'Overweight!';
                rangeElement.style.color = 'rgb(227, 212, 47)';
            } else {
                rangeElement.textContent = 'Obese!';
                rangeElement.style.color = 'rgb(255, 0, 0)';
            }
    
            // Update the main result paragraph
            rangeResult.textContent = 'You are';
        } catch (error) {
            console.error('Error in displayBMIRange:', error);
        }
    }
    

    function resetInputs() {
        heightInput.value = '';
        weightInput.value = '';
        bmiResult.textContent = '0.0';
        rangeResult.textContent = 'Please enter your height and weight.';
    }
});
