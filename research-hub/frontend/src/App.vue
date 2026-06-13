<template>
  <div class="min-h-screen bg-slate-950 text-slate-200 antialiased">
    <header class="sticky top-0 z-40 border-b border-white/5 bg-slate-950/80 backdrop-blur">
      <div class="mx-auto flex h-14 max-w-7xl items-center gap-3 px-4 sm:px-6">
        <RouterLink to="/" class="flex items-center gap-2.5 group">
          <span
            class="grid h-8 w-8 place-items-center rounded-lg bg-gradient-to-br from-sky-400 to-indigo-600 text-sm font-black text-white shadow-lg shadow-indigo-500/20"
          >R</span>
          <span class="text-sm font-semibold tracking-wide text-slate-100 group-hover:text-white">
            Research <span class="text-sky-400">Hub</span>
          </span>
        </RouterLink>
        <span class="ml-2 hidden rounded-full border border-white/10 px-2 py-0.5 text-[10px] uppercase tracking-widest text-slate-500 sm:inline">
          csv intelligence
        </span>
      </div>
    </header>
    <main class="mx-auto max-w-7xl px-4 py-8 sm:px-6">
      <RouterView />
    </main>
  </div>
</template>
