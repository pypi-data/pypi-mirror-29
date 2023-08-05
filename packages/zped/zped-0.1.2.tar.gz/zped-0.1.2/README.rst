======================================
Zoidberg's Preempting Event Dispatcher
======================================

--------------------------
Why you shouldn't use this
--------------------------

ZPED let's you do some truly silly stuff with event dispatching. There's a built-in decorator that will create and execute pre/post execution events on functions, which is pretty cool! Until you realize that your event listeners can arbitrarily modify the execution of your code by raising exceptions. A pre-execution event can completely modify the data sent to the executing function, or even the data sent to other listeners (since they're executed in serial). The same event can even stop execution entirely and force return a value. A post-execution event can do similar. It's insane, it's terrible, it will make your applications /really/ hard to debug.

---------------------
Why I even wrote this
---------------------

I'm in the process of writing a static website generator based on Flask, and I needed a good way to let plugins tie into the core system. One of the better days to do this is with event dispatching! So I started writing a simple dispatcher, because using an external library for that seemed silly. Then I thought, "If I were insane and writing a plugin to heavily modify the generator's internals, but didn't want to fork the code or monkeypatch... what would I need?" ZPED is the culmination of that, and entirely too much coffee.

--------------------------------------------------------------
Ok, but... I don't /have/ to use the bad parts of this, right?
--------------------------------------------------------------

No, but power corrupts.

--------------------------
Just tell me how to use it
--------------------------

Look at the tests, I'll write some docs later.
