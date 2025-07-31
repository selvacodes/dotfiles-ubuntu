return {{'dmmulroy/ts-error-translator.nvim'}, {
    'prichrd/netrw.nvim',
    config = function()
        require'netrw'.setup {
            -- Put your configuration here, or leave the object empty to take the default
            -- configuration
            use_devicons = true, -- Uses nvim-web-devicons if true, otherwise use the file icon specified above
            mappings = {} -- Custom key mappings
        }

    end
}}
