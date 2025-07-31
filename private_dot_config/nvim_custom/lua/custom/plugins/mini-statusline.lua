local M = {
  'echasnovski/mini.statusline',
  event = 'VeryLazy',
  config = function()
    local mini_statusline = require 'mini.statusline'
    vim.opt.laststatus = 3

    local opts = {
      use_icons = true,
      content = {
        active = function()
          local mode, mode_hl = mini_statusline.section_mode {
            trunc_width = 999,
          }
          local git = mini_statusline.section_git {
            trunc_width = 999,
          }
          local filename = mini_statusline.section_filename {
            trunc_width = 0,
          }
          local fileinfo = mini_statusline.section_fileinfo {
            trunc_width = 120,
          }
          local location = mini_statusline.section_location {
            trunc_width = 75,
          }
          local search = mini_statusline.section_searchcount {
            trunc_width = 75,
          }

          local arrow_indicator = function()
            return require('arrow.statusline').text_for_statusline_with_icons()
          end
          local lsp_progress = function()
            if #vim.lsp.get_active_clients() == 0 then
              return ''
            end

            local lsp = vim.lsp.util.get_progress_messages()[1]
            if lsp then
              local name = lsp.name or ''
              local msg = lsp.message or ''
              local percentage = lsp.percentage or 0
              local title = lsp.title or ''
              return string.format(' %%<%s: %s %s (%s%%%%) ', name, title, msg, percentage)
            end
            return ''
          end

          return mini_statusline.combine_groups {
            {
              hl = mode_hl,
              strings = { mode },
            },
            {
              hl = 'MiniStatuslineDevinfo',
              strings = { git },
            },
            {
              hl = 'MiniStatuslineDevinfo',
              strings = { arrow_indicator() },
            },
            '%<',
            {
              hl = 'MiniStatuslineFilename',
              strings = { filename },
            }, -- Mark general truncate point
            '%=', -- End left alignment
            '%<',
            {
              hl = 'MiniStatuslineFileinfo',
              strings = { lsp_progress(), fileinfo },
            },
            {
              hl = mode_hl,
              strings = { search, location },
            },
          }
        end,
      },
      set_vim_settings = false,
    }
    mini_statusline.setup(opts)
  end,
}

return M
