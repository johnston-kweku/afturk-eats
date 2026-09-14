
document.addEventListener('DOMContentLoaded', function () {
    const roleCards = document.querySelectorAll('.role-card');
    const generateBtn = document.getElementById('generate-invite-btn');
    const errorEl = document.getElementById('generate-error');
    const resultEl = document.getElementById('generate-result');
    const linkOutput = document.getElementById('invite-link-output');
    const copyBtn = document.getElementById('copy-invite-btn');

    let selectedRole = null;


    const GENERATE_INVITE_URL = '/invite/';

    function selectRole(role, clickedCard) {
        selectedRole = role;

        roleCards.forEach(function (card) {
            card.classList.remove('border-cyprus-700', 'bg-cyprus-700/5');
            card.classList.add('border-cyprus-100');
        });

        clickedCard.classList.remove('border-cyprus-100');
        clickedCard.classList.add('border-cyprus-700', 'bg-cyprus-700/5');

        generateBtn.disabled = false;
    }

    roleCards.forEach(function (card) {
        card.addEventListener('click', function () {
            selectRole(card.dataset.role, card);
        });
    });



    function showError(message) {
        errorEl.textContent = message;
        errorEl.classList.remove('hidden');
        resultEl.classList.add('hidden');
        resultEl.classList.remove('flex');
    }

    function showResult(inviteUrl) {
        errorEl.classList.add('hidden');
        linkOutput.value = inviteUrl;
        resultEl.classList.remove('hidden');
        resultEl.classList.add('flex');
    }

    generateBtn.addEventListener('click', function () {
        if (!selectedRole) {
            return;
        }

        generateBtn.disabled = true;
        generateBtn.textContent = 'Generating...';

        fetch(GENERATE_INVITE_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({ role: selectedRole }),
        })
            .then(function (response) {
                if (!response.ok) {
                    throw new Error('Failed to generate invite link');
                }
                return response.json();
            })
            .then(function (data) {

                showResult(data.invitation_link);
            })
            .catch(function (err) {
                showError(err.message || 'Something went wrong. Please try again.');
            })
            .finally(function () {
                generateBtn.disabled = false;
                generateBtn.textContent = 'Generate Invite Link';
            });
    });

    copyBtn.addEventListener('click', function () {
        if (!linkOutput.value) {
            return;
        }
        navigator.clipboard.writeText(linkOutput.value).then(function () {
            const original = copyBtn.textContent;
            copyBtn.textContent = 'Copied!';
            setTimeout(function () {
                copyBtn.textContent = original;
            }, 1500);
        });
    });
});