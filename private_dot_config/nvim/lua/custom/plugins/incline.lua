local field_format = {
  name = {
    guifg = '#a0a0a0',
    guibg = '#282828',
  },
  num = {
    guifg = '#968c81',
  },
  modified = {
    guifg = '#d6991d',
  },
  blocks = {
    gui = 'bold',
    guifg = '#070707',
  },
}
return {
  'b0o/incline.nvim',
  enabled = true,
  dependencies = {
    { 'echasnovski/mini.statusline' },
    { 'nvim-tree/nvim-web-devicons' },
  },
  config = function()
    require('incline').setup {
      render = function(props)
        local function get_git_diff()
          local icons = { removed = '-', changed = '*', added = '+' }
          icons['changed'] = icons.modified
          local signs = vim.b[props.buf].gitsigns_status_dict
          local labels = {}
          if signs == nil then
            return labels
          end
          for name, icon in pairs(icons) do
            if tonumber(signs[name]) and signs[name] > 0 then
              table.insert(labels, { icon .. signs[name] .. ' ', group = 'Diff' .. name })
            end
          end
          if #labels > 0 then
            table.insert(labels, { '| ' })
          end
          return labels
        end

        local buffullname = vim.api.nvim_buf_get_name(props.buf)
        local bufname_t = vim.fn.fnamemodify(buffullname, ':t')
        local bufname = (bufname_t and bufname_t ~= '') and bufname_t or '[No Name]'

        local mini_statusline = require 'mini.statusline'
        local diagnostics = mini_statusline.section_diagnostics {
          trunc_width = 120,
        }
        local git = mini_statusline.section_git {
          trunc_width = 999,
        }

        local display_bufname = vim.tbl_extend('force', { bufname, ' ' }, field_format.name)

        -- modified indicator
        local modified_icon = {}
        if vim.api.nvim_get_option_value('modified', { buf = props.buf }) then
          modified_icon = vim.tbl_extend('force', { '● | ' }, field_format.modified)
          display_bufname.guifg = field_format.modified.guifg
        else
          table.insert(display_bufname, { '| ' })
        end

        -- example: █▓   incline-nvim.lua 13  ▓█
        return {
          display_bufname,
          modified_icon,
          get_git_diff(),
          diagnostics,
          ' ',
        }
      end,
      window = {
        padding = {
          left = 0,
          right = 0,
        },
        margin = {
          horizontal = 0,
          vertical = 1,
        },
        placement = {
          horizontal = 'right',
          vertical = 'top',
        },
      },
    }
  end,
}
