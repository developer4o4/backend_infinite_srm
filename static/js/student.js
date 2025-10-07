// O'chirishni tasdiqlash
function confirmDelete(name) {
    return confirm(name + " ni o‘chirishni xohlaysizmi?");
}

// Form validation
document.addEventListener("DOMContentLoaded", function () {
    let forms = document.querySelectorAll(".student-form");
    forms.forEach(form => {
        form.addEventListener("submit", function (e) {
            let inputs = form.querySelectorAll("input[required], select[required]");
            let valid = true;

            inputs.forEach(input => {
                if (!input.value.trim()) {
                    input.style.border = "2px solid red";
                    valid = false;
                } else {
                    input.style.border = "1px solid #ccc";
                }
            });

            if (!valid) {
                e.preventDefault();
                alert("Iltimos, barcha maydonlarni to‘ldiring!");
            }
        });
    });
});
