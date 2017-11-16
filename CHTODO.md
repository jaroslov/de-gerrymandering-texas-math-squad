TODO:
1. Factor JS out into a separate file.
2. Factor out globals into an init() call.
3. Split Ch2 into 2 & 3.
4. Redo reflector with new scheme: unused=0, filled>0, borders<0.
5. Allow line erasure (post 4) by filtering/patching-up the border's lineloop. The basic idea is to render the line segments as negative numbers. Then, when erasing we can build a filter-list and remove those values by index with a copy. We do need to track 'end-of-painting' properly.
6. Render borders in the background, rather than the foreground.
7. Make the status information a proper HUD, floating, on the left.
8. Move to a tiling architecture for rendering---this interacts in non-trivial ways with pan/zoom.
