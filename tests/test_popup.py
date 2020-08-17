from unittest import mock

from pathfinder.client.popup import _neovim_popup, _vim_popup, open_popup


@mock.patch("pathfinder.client.popup._vim_popup")
@mock.patch("pathfinder.client.popup._neovim_popup")
@mock.patch(
    "pathfinder.client.popup.vim.eval",
    side_effect=lambda x: {
        "line('.')": "1",
        "has('nvim-0.4')": "1",
        "has('popupwin')": "0",
    }[x],
)
def test_open_popup_neovim(vim_eval, neovim_popup, vim_popup):
    open_popup(mock.sentinel.text)
    vim_eval.assert_any_call("has('nvim-0.4')")
    neovim_popup.assert_called_once_with(mock.sentinel.text, "+1")
    vim_popup.assert_not_called()


@mock.patch("pathfinder.client.popup._vim_popup")
@mock.patch("pathfinder.client.popup._neovim_popup")
@mock.patch(
    "pathfinder.client.popup.vim.eval",
    side_effect=lambda x: {
        "line('.')": "2",
        "has('nvim-0.4')": "0",
        "has('popupwin')": "1",
    }[x],
)
def test_open_popup_vim(vim_eval, neovim_popup, vim_popup):
    open_popup(mock.sentinel.text)
    vim_eval.assert_any_call("has('popupwin')")
    neovim_popup.assert_not_called()
    vim_popup.assert_called_once_with(mock.sentinel.text, "-1")


@mock.patch("pathfinder.client.popup._vim_popup")
@mock.patch("pathfinder.client.popup._neovim_popup")
@mock.patch(
    "pathfinder.client.popup.vim.eval",
    side_effect=lambda x: {
        "line('.')": "3",
        "has('nvim-0.4')": "0",
        "has('popupwin')": "0",
    }[x],
)
def test_open_popup_echo(vim_eval, neovim_popup, vim_popup):
    open_popup(mock.sentinel.text)
    neovim_popup.assert_not_called()
    vim_popup.assert_not_called()


@mock.patch("pathfinder.client.popup.vim.vars", {"pf_popup_time": b"2000"})
def test_vim_popup():
    popup_create = mock.MagicMock(name='vim.Function("popup_create")')

    with mock.patch("pathfinder.client.popup.vim.Function", return_value=popup_create):
        _vim_popup("hello world", "+1")

    popup_create.assert_called_once_with(
        "hello world",
        {
            "line": "cursor+1",
            "col": "cursor",
            "wrap": False,
            "padding": (0, 1, 0, 1),
            "highlight": "PathfinderPopup",
            "time": 2000,  # Mocked in decorator
            "zindex": 1000,
        },
    )


@mock.patch("pathfinder.client.popup.vim.vars", {"pf_popup_time": b"2000"})
@mock.patch("pathfinder.client.popup.vim.eval")
@mock.patch("pathfinder.client.popup.vim.api.win_set_option")
@mock.patch(
    "pathfinder.client.popup.vim.api.open_win", return_value=mock.sentinel.window
)
@mock.patch("pathfinder.client.popup.vim.api.buf_set_lines")
@mock.patch(
    "pathfinder.client.popup.vim.api.create_buf", return_value=mock.sentinel.buffer
)
def test_neovim_popup(create_buf, buf_set_lines, open_win, win_set_option, vim_eval):
    type(open_win.return_value).handle = mock.PropertyMock(return_value="window handle")

    _neovim_popup("hello world", "-1")

    create_buf.assert_called_once_with(False, True)
    buf_set_lines.assert_called_once_with(
        mock.sentinel.buffer, 0, -1, True, [" hello world "]
    )
    open_win.assert_called_once_with(
        mock.sentinel.buffer,
        0,
        {
            "relative": "cursor",
            "row": -1,
            "col": 0,
            "style": "minimal",
            "focusable": 0,
            "height": 1,
            "width": 13,
        },
    )
    win_set_option.assert_called_once_with(
        mock.sentinel.window, "winhl", "Normal:PathfinderPopup"
    )
    vim_eval.assert_called_once_with(
        "timer_start(2000, {-> nvim_win_close(window handle, 1)})"
    )
