// دالة لشطب المهمة عند الضغط على زر إنجاز أو النص
function toggleTask(element) {
    const li = element.closest('.task-item');
    li.classList.toggle('completed');
}

function toggleTaskButton(button) {
    const li = button.closest('.task-item');
    li.classList.toggle('completed');
}

let currentTaskId = null;

// فتح نافذة الحذف بتأثير سلس
function openDeleteModal(taskId) {
    currentTaskId = taskId;
    const modal = document.getElementById('deleteModal');
    modal.classList.add('active');
}

// إغلاق نافذة الحذف
function closeDeleteModal() {
    const modal = document.getElementById('deleteModal');
    modal.classList.remove('active');
    currentTaskId = null;
}

// تنفيذ الحذف الفعلي وإرسال طلب لـ Flask Backend
document.getElementById('confirmDeleteBtn').addEventListener('click', function () {
    if (currentTaskId) {
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = '/delete_task/' + currentTaskId;
        document.body.appendChild(form);
        form.submit();
    }
});