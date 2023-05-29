const requiredPercentage = 85;

document.getElementById('calculate').addEventListener('click', () => {
    const currentAttendance = parseFloat(document.getElementById('currentAttendance').value);
    const totalClasses = parseInt(document.getElementById('totalClasses').value);
    const remainingClasses = parseInt(document.getElementById('remainingClasses').value);
    const resultElement = document.getElementById('result');
  
    if (!isNaN(currentAttendance) && !isNaN(totalClasses) && !isNaN(remainingClasses) && totalClasses > 0 && remainingClasses >= 0) {
      const attendedClasses = Math.round((currentAttendance / 100) * totalClasses);
  
      // Calculate the number of classes to attend out of remaining classes to maintain 85% attendance.
      const requiredClasses = ((requiredPercentage / 100) * (totalClasses + remainingClasses)) - attendedClasses;
  
      // Calculate the number of classes that can be skipped.
      const skippableClasses = Math.max(0, remainingClasses - Math.ceil(requiredClasses));
  
      resultElement.innerHTML = `<p>You can skip <strong>${skippableClasses}</strong> classes without falling below the required attendance percentage over a period of ${remainingClasses/6} working days.</p>`;
      resultElement.classList.add('alert');
      resultElement.classList.add('alert-info');
    } else {
      resultElement.innerHTML = '<p>Please enter valid numbers for all fields.</p>';
      resultElement.classList.add('alert');
      resultElement.classList.add('alert-warning');
    }
});