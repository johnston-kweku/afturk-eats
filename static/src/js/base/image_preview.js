

document.addEventListener('DOMContentLoaded', function () {
    function wireImagePreview(inputId, previewId, placeholderId) {
        const input = document.getElementById(inputId);
        const preview = document.getElementById(previewId);
        const placeholder = document.getElementById(placeholderId);

        if (!input || !preview || !placeholder) {
            return;
        }

        input.addEventListener('change', function () {
            const file = input.files && input.files[0];

            if (!file) {
                preview.src = '';
                preview.classList.add('hidden');
                placeholder.classList.remove('hidden');
                return;
            }

            const reader = new FileReader();
            reader.onload = function (event) {
                preview.src = event.target.result;
                preview.classList.remove('hidden');
                placeholder.classList.add('hidden');
            };
            reader.readAsDataURL(file);
        });
    }

    wireImagePreview('ghana_card_image', 'ghana_card_preview', 'ghana_card_placeholder');
    wireImagePreview('profile_image', 'profile_image_preview', 'profile_image_placeholder');
    wireImagePreview('id_image', 'item_image_preview', 'item_image_placeholder')
});