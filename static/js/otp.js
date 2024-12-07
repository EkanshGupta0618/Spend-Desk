document.addEventListener("DOMContentLoaded", () => {
  const inputs = document.querySelectorAll(".otp-input input");
  const verifyBtn = document.getElementById("verify-btn");

  inputs.forEach((input, index) => {
    input.addEventListener("input", (e) => {
      const nextInput = inputs[index + 1];
      const prevInput = inputs[index - 1];

      // Move to the next input if valid
      if (e.target.value && nextInput) {
        nextInput.focus();
      }

      // Allow backspace to go to previous input
      if (
        e.inputType === "deleteContentBackward" &&
        !e.target.value &&
        prevInput
      ) {
        prevInput.focus();
      }

      // Enable/Disable button based on all fields being filled
      const otpFilled = Array.from(inputs).every(
        (input) => input.value.trim() !== ""
      );
      verifyBtn.disabled = !otpFilled;
    });

    // Ensure only numbers are entered
    input.addEventListener("keypress", (e) => {
      if (!/[0-9]/.test(e.key)) {
        e.preventDefault();
      }
    });
  });
});
