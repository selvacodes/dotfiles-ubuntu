local M = {
  'nvimdev/lspsaga.nvim',
  config = function()
    require('lspsaga').setup {
      ui = {},
      lightbulb = {
        virtual_text = true,
        sign = false,
        debounce = 10,
      },
      symbol_in_winbar = {
        enable = false,
      },
      rename = {
        in_select = false,
      },
    }
    vim.keymap.set('n', 'K', '<cmd>Lspsaga hover_doc<CR>', { desc = 'Hover Documentation' })
    vim.keymap.set('n', 'F', '<cmd>Lspsaga finder<CR>', { desc = 'Finder' })
    vim.keymap.set('n', 'gsd', '<cmd>Lspsaga peek_definition<CR>', { desc = 'Peek Definition' })
    vim.keymap.set('n', '<leader>rn', '<cmd>Lspsaga rename<CR>', { desc = 'Rename' })
    -- vim.keymap.set('n', '<leader>ca', '<cmd>Lspsaga code_action<CR>', { desc = 'Code Action' })
  end,
  dependencies = {
    'nvim-treesitter/nvim-treesitter', -- optional
    'nvim-tree/nvim-web-devicons', -- optional
  },
}

return M
