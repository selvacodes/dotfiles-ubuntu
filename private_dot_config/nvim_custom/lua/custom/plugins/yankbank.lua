local M = {
  'ptdewey/yankbank-nvim',
  config = function()
    require('yankbank').setup()
    vim.keymap.set('n', '<leader>y', '<cmd>YankBank<CR>', { noremap = true })
  end,
}

return M
