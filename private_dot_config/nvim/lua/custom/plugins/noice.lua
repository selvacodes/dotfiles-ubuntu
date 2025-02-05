return {
  'folke/noice.nvim',
  event = 'VeryLazy',
  opts = {},
  dependencies = { -- if you lazy-load any plugin below, make sure to add proper `module="..."` entries
    'MunifTanjim/nui.nvim', -- OPTIONAL:
    --   `nvim-notify` is only needed, if you want to use the notification view.
    --   If not available, we use `mini` as the fallback
    'rcarriga/nvim-notify',
  },
  config = function()
    require('noice').setup {
      -- cmdline = {
      --     view = "cmdline"
      -- },
      presets = {
        bottom_search = true, -- use a classic bottom cmdline for search
        command_palette = true, -- position the cmdline and popupmenu together
        long_message_to_split = false, -- long messages will be sent to a split
        inc_rename = false, -- enables an input dialog for inc-rename.nvim
        lsp_doc_border = true,
      },
      lsp = {
        progress = {
          enabled = false,
        },
      },
      views = {
        mini = {
          win_options = { winblend = 0 },
          timeout = 2000,
        },
        virtualtext = {
          backend = 'virtualtext',
        },
        -- cmdline_popup = {
        --   position = {
        --     row = 8,
        --     col = '80%',
        --   },
        --   size = {
        --     width = 'auto',
        --     height = 'auto',
        --   },
        -- },
        -- popupmenu = {
        --   position = {
        --     row = 15,
        --     col = '50%',
        --   },
        --   size = {
        --     width = 'auto',
        --     height = 'auto',
        --   },
        --   border = {
        --     style = 'rounded',
        --     padding = { 0, 1 },
        --   },
        --   win_options = {
        --     winhighlight = { Normal = 'Normal', FloatBorder = 'DiagnosticInfo' },
        --   },
        -- },
      },
    }
  end,
}
