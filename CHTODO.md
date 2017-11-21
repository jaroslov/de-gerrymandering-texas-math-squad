TODO:
1. Redo reflector with new scheme: unused=0, filled>0, borders<0.
2. Make the status information a proper HUD, floating, on the left.
3. Move to a tiling architecture for rendering---this interacts in non-trivial ways with pan/zoom.
4. Render borders offscreen, and manually composite on screen. This gives the following painters algorithm:
    (a) Map.
    (2) Borders.
    (3) Population.
5. Send a copy of the commands (data?) upstream to a server.
