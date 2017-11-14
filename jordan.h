#ifndef JORDAN_H
#define JORDAN_H

/*

    High level overview of the GUI provides

    +-------------------------------+
    | (x)(-)(^) TITLE               |
    +-------------------------------+
    |                               |
    |  :                            |
    |  |                 +--------+ | \
    |  |                 |  INFO  | | |
    | -*                 | K VVVV | | > Key-value HUD
    |   \                | K VVVV | | |
    |    *-----*         +--------+ | /
    |           \                   |
    |            *<-+               |
    |            :  |          <-------- Surface supports pan & zoom via drag & double click.
    |            :  |               |
    |               |               |
    |               |    |------50| | } Legend (scrollbar scale)
    +---------------|---------------+
                    |
                    |
                Vertices, edges, and
                polygons are first-class
                primitives. All three
                use an index buffer to
                simplify tracking aliased
                vertices.

    The GUI will allow arbitrary composited
    background layers. How atlasing (the
    background textures) are handled will be
    determined later.

*/

//
// When the UI is updated, it will call back
// into the driver's code, informing the driver
// of updates to the UI.
//
// All 'verb' actions (VertexMove, EdgeMove),
// are telling the driver's code the intent of
// the user's action. However, the representation
// of GUI elements does not change until the
// driver updates Jordan's state. For instance,
// if 'VertexMove' occurs, then the driver must
// change the value of the vertices before the user
// will see an update to the UI.
//
// If the driver doesn't want to receive a given
// form of state update, then the driver should leave
// that function pointer null.
//
typedef struct JordanCallback
{
    void*       Handle;

    // The indexed node is being dragged by a step of delta.
    int       (*VertexMove)     (void* Handle, int vtx, double delta[2]);

    // The indexed edge is being dragged by a step of delta.
    // Edge moves are always perpendicular to the edge.
    int       (*EdgeMove)       (void* Handle, int edge[2], double delta);

    int       (*VertexDelete)   (void* Handle, int vtx);
    // Request to add a vertex on edge, at offset baryI from
    // vertex edge[0].
    int       (*VertexInsert)   (void* Handle, int edge[2], double baryI);

    // If polyHints are used, polygons can be selected.
    int       (*PolySelect)     (void* Handle, int poly);

    // The following callbacks into the driver tell the
    // driver basic facts about the 'background' of the UI.

    // The size of the screen in texels (screen elements).
    int       (*ScreenSize)     (void* Handle, int widthInTexels, int heightInTexels);

    // The location of the canvas' upper-left coordinate
    // with respect to the absolute canvas size. The canvas
    // is always a square of size 1x1. The 'nits' of the location
    // are in terms of 48b value. Thus, these values are always
    // in the range [0,0xFFFFFFFFFFFF]
    int       (*CanvasLocation) (void* Handle, long long offX, long long offY);

    // A scale factor of '0' means we're as far away from the map as
    // we're allowed to be. Each 'step' of the scale factor is a factor of 2.
    // Thus, a scale factor of '5' is 2^32 times 'zoomed' in.
    int       (*Scale)          (void* Handle, int scaleFactor);

    // Current pointer position.
    int       (*PointerMove)    (void* Handle, int X, int Y);
    // In theory, a number of the devices support specific "motions"
    // for pan, zoom, and rotate.
    int       (*Pan)            (void* Handle, double delta[2]);
    int       (*Zoom)           (void* Handle, double scale);
    int       (*Rotate)         (void* Handle, double degrees);
} JordanCallback;

//
// Jordan's internal state is held in an opaque record, Jordan.
//
typedef struct Jordan Jordan;

// Create or destroy an instance of Jordan.
typedef struct JordanOptions
{
    int             ShowHelp;
} JordanOptions;
extern int          jordanParseOptions(int argc, char** argv, JordanOptions*);
extern Jordan*      jordanMake(JordanOptions*);
extern int          jordanFree(Jordan*);

// The 'Curves' record is shared between Jordan and the
// driver. This means that updates to Curves will be
// reflected in the Jordan UI on the next refresh of the
// UI.
typedef struct JordanCurve
{
    double         *vertices;   // Raw vertex data; double v[N][2];
    int             numEdges;   // Number of edges to display.
    int            *edges;      // Edge reference into vertex data; int e[K][2];
    int             numPolys;   // If the edges are coalesced into well-defined
    int            *polyHint;   // polygons, then set the numPolys>0. Each polyHint
                                // is a number of edges. That is, polyHint[0] defines
                                // edges[0]--edges[polyHint[0]-1] to be a polygon.
                                // Then polyHint[1] defines edges[polyHint[0]]--
                                // edges[polyHint[0]+polyHint[1]-1] to be the next
                                // polygon.
} JordanCurve;

//
// Construction of the Atlas isn't well-defined yet (I'm still learning
// NK & GLFW). However, it will be done "by index". Jordan will support
// at least 4 overlays. It is the responsibility of the user to make
// sure the overlays support stenciling or transparency.
//
typedef struct JordanAtlas
{
    int             numTextures;
    int            *indices;
} JordanAtlas;

//
// The remainder of the Jordan API is for the basic nuts-and-bolts of theming.
//
typedef struct JordanTheme
{
    unsigned char   BackgroundColor[4];         // White.
    unsigned char   ForegroundColor[4];         // Black.
    unsigned char   UnselectedVertexColor[4];   // Gray.
    unsigned char   UnselectedEdgeColor[4];     // Gray.
    unsigned char   SelectedVertexColor[4];     // Blue.
    unsigned char   SelectedEdgeColor[4];       // Blue.
    unsigned char   UnselectedPolyColor[4];     // Light gray.
    unsigned char   SelectedPolyColor[4];       // Light blue.
} JordanTheme;

//
// When the user selects a polygon, or their mouse is hovering over a given
// area, we can display text information. This information is in the form
// of a key-value set.
//
typedef struct JordanInfo
{
    int             numKeys;
    const char**    Keys;
    const char**    Values;
} JordanInfo;

//
// Start the UI.
//
extern int          jordanStart(Jordan*, JordanCallback*, JordanCurve*, JordanAtlas*, JordanTheme*, JordanInfo*);

#endif//JORDAN_H
