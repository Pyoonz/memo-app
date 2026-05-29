//　　メモアプリの JavaScript (次の章で実装します)
// メモアプリを動かすコード

//  ① --- DOM要素の取得 ---
const memoForm = document.getElementById("memo-form");
const memoTitle = document.getElementById("memo-title");
const memoBody = document.getElementById("memo-body");
const memoId = document.getElementById("memo-id");
const memoList = document.getElementById("memo-list");
const btnCreate = document.getElementById("btn-create");
const btnUpdate = document.getElementById("btn-update");
const btnDelete = document.getElementById("btn-delete");
const btnCancel = document.getElementById("btn-cancel");


// ② --- メモ一覧を読み込む ---
async function fetchMemos() {
    const response = await fetch("/api/memos");
    const memos = await response.json();

    // メモ一覧エリアをクリア
    memoList.innerHTML = "";

    if (memos.length === 0) {
        memoList.innerHTML = '<p class="empty-message">メモがまだありません。上のフォームから作成してみましょう。</p>';
        return;
    }

    // 各メモをカードとして表示
    memos.forEach(function (memo) {
        const card = document.createElement("div");
        card.className = "memo-card";
        card.innerHTML =
            "<h3>" + memo.title + "</h3>" +
            "<p>" + memo.body + "</p>" +
            '<span class="memo-date"> 更新: ' + memo.updated_at + "</span>";

        // カードをクリックしたらメモを選択
        card.addEventListener("click", function () {
            selectMemo(memo);
            // 選択状態のスタイルをつける
            document.querySelectorAll(".memo-card").forEach(function (c) {
                c.classList.remove("selected");
            });
            card.classList.add("selected");
        });

        memoList.appendChild(card);
    });
}

// ③ --- メモを作成する
async function createMemo() {
    var title = memoTitle.value.trim();
    var body = memoBody.value.trim();

    if (!title || !body) {
        alert("タイトルと本文を入力してください")
        return;
    }

    await fetch("/api/memos", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ title: title, body: body }),
    });

    resetForm();
    fetchMemos();

}


// ④ --- メモを選択する (編集モードにする) ---
function selectMemo(memo) {
    memoId.value = memo.id;
    memoTitle.value = memo.title;
    memoBody.value = memo.body;

    //  ボタンの切り替え
    btnCreate.disabled = true;
    btnUpdate.disabled = false;
    btnDelete.disabled = false;
}

// ⑤ --- メモを更新する ---
async function updateMemo() {
    var id = memoId.value;
    var title = memoTitle.value.trim();
    var body = memoBody.value.trim();

    if (!title || !body) {
        alert("タイトルと本文を入力してください。");
        return;
    }

    await fetch("/api/memos/" + id, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ title: title, body: body }),
    });

    resetForm();
    fetchMemos();
}

// ⑥ --- メモを削除する ---
async function deleteMemo() {
    var id = memoId.value;

    if (!confirm("このメモを削除しますか？")) {
        return;
    }

    await fetch("/api/memos/" + id, {
        method: "DELETE",
    });

    resetForm();
    fetchMemos();
}

// ⑦ --- フォームをリセットする ---
function resetForm() {
    memoId.value = "";
    memoTitle.value = "";
    memoBody.value = "";

    // ボタンの状態を初期状態に戻す 
    btnCreate.disabled = false;
    btnUpdate.disabled = true;
    btnDelete.disabled = true;

    // 選択状態を解除
    document.querySelectorAll(".memo-card").forEach(function (c) {
        c.classList.remove("selected")
    });
}

// ⑧ --- イベントリスナーの登録 ---

// --- フォーム送信ボタン（作成ボタン）
memoForm.addEventListener("submit", function (e) {
    e.preventDefault();
    createMemo();
});

//更新ボタン
btnUpdate.addEventListener("click", updateMemo);

// 削除ボタン
btnDelete.addEventListener("click", deleteMemo);

// キャンセルボタン
btnCancel.addEventListener("click", resetForm);

// ページ読み込み時にメモ一覧を取得
fetchMemos();
