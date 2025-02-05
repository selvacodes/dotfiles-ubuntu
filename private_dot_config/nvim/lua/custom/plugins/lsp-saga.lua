local M = {
  'nvimdev/lspsaga.nvim',
  config = function()
    require('lspsaga').setup {
      ui = {},
      lightbulb = {
        virtual_text = false,
        sign = false,
      },
      symbol_in_winbar = {
        enable = false,
      },
    }
    vim.keymap.set('n', 'K', '<cmd>Lspsaga hover_doc<CR>', { desc = 'Hover Documentation' })
  end,
  dependencies = {
    'nvim-treesitter/nvim-treesitter', -- optional
    'nvim-tree/nvim-web-devicons', -- optional
  },
}

return M
