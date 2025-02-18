# tests/test_view.py

from src.view import DummyView

def test_dummy_view_choose_from_list():
    dummy = DummyView()
    # ダミービューは常に選択肢 0 を返す
    items = ['a', 'b', 'c']
    choice = dummy.choose_from_list("選択してください:", items)
    assert choice == 0
    # 表示されたメッセージが記録されていることを確認（任意）
    assert "選択してください:" in dummy.messages[0]

