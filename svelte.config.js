/**
 * from https://kit.svelte.dev/docs/adapter-static
 */
import adapter from '@sveltejs/adapter-static'
import preprocess from 'svelte-preprocess'

export default {
    preprocess: preprocess(),
    kit: {
        paths: {
            base: '/PhysicsProject',
            relative: false
        },
        adapter: adapter({
            // default options are shown. On some platforms
            // these options are set automatically — see below
            pages: 'build',
            assets: 'build',
            fallback: null,
            precompress: false,
            strict: true
        })
    }
}
