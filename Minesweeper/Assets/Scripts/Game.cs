using UnityEngine;
using UnityEngine.UI;
using TMPro;
using AustinHarris.JsonRpc;

public class Game : MonoBehaviour
{
    [SerializeField] private Slider widthAndHeightSlider;
    [SerializeField] private Slider mineSlider;
    [SerializeField] private TextMeshProUGUI widthAndHeightSliderText;
    [SerializeField] private TextMeshProUGUI mineSliderText;
    [SerializeField] private TextMeshProUGUI winLoseText;
    
    public int width = 16;
    public int height = 16;
    public int mineCount = 32;
    public int tempWidth;
    public int tempHeight;
    public int tempMines;

    private Board board;
    private Cell[,] state;
    private bool gameover;

    private Color background = new Color32(69, 255, 231, 0);

    class Rpc : JsonRpcService
    {
        public Game game;

        public Rpc(Game game)
        {
            this.game = game;
        }

        [JsonRpcMethod]
        void Say(string message)
        {
            Debug.Log($"you sent a {message}");
        }

        [JsonRpcMethod]
        int GetWidthHeight()
        {
            return game.width;
        }

        [JsonRpcMethod]
        int GetCell(int x, int y)
        {
            if (game.state[x, y].revealed)
            {
                if (game.state[x, y].type == Cell.Type.Mine)
                    return -2;
                else if (game.state[x, y].type == Cell.Type.Number)
                    return game.state[x, y].number;
                else if (game.state[x, y].type == Cell.Type.Empty)
                    return 0;
                else
                    return -3;
            }
            else
            {
                return -1;
            }
        }

        [JsonRpcMethod]
        string GetAllCells()
        {
            string output = "";
            for (int j = game.width - 1; j >= 0; j--)
            {
                output = output + "\n";
                for (int i = 0; i < game.width; i++)
                {
                    if (game.state[i, j].revealed)
                    {
                        if (game.state[i, j].type == Cell.Type.Mine)
                            output = output + "-2 ";
                        else if (game.state[i, j].type == Cell.Type.Number)
                            output = output + game.state[i, j].number.ToString()+" ";
                        else if (game.state[i, j].type == Cell.Type.Empty)
                            output = output + "0 ";
                        else
                            output = output + "-3 ";
                    }
                    else
                    {
                        output = output + "-1 ";
                    }
                }
            }
            return output;
        }
    }
    Rpc rpc;

    private void OnValidate()
    {
        mineCount = Mathf.Clamp(mineCount, 0, width * height);
    }

    private void Awake()
    {
        board = GetComponentInChildren<Board>();
    }

    private void Start()
    {
        rpc = new Rpc(this);
        InitTemp();
        NewGame();
        InitSliderListeners();
    }

    private void NewGame()
    {
        board.ClearTiles();
        InitFromTemp();
        state = new Cell[width, height];
        gameover = false;
        winLoseText.text = "";
        GenerateCells();
        GenerateMines();
        GenerateNumbers();
        Camera.main.transform.position = new Vector3(width / 2f, height / 2f, -10f);
        int size;
        if (height <= 16 && width <= 16){
            size = 10;
        }
        else
        {
            size = 12;
        }
        Camera.main.orthographicSize = size;
        Camera.main.backgroundColor = background;
            
        board.Draw(state);
    }

    private void GenerateCells()
    {
        for(int x = 0; x < width; x++)
        {
            for(int y = 0; y < height; y++)
            {
                Cell cell = new Cell();
                cell.position = new Vector3Int(x, y, 0);
                cell.type = Cell.Type.Empty;
                state[x, y] = cell;
            }
        }
    }

    private void GenerateMines()
    {
        for(int i = 0; i < mineCount; i++)
        {
            int x = Random.Range(0, width);
            int y = Random.Range(0, height);

            while(state[x, y].type == Cell.Type.Mine)
            {
                x = Random.Range(0, width);
                y = Random.Range(0, height);
            }

            state[x, y].type = Cell.Type.Mine;
            //state[x, y].revealed = true;
        }
    }

    private void GenerateNumbers()
    {
        for(int x = 0; x < width; x++)
        {
            for(int y = 0; y < height; y++)
            {
                Cell cell = state[x, y];
                if(cell.type == Cell.Type.Mine)
                {
                    continue; //skips to next iteration
                }
                cell.number = CountMines(x, y);
                if(cell.number > 0)
                {
                    cell.type = Cell.Type.Number;
                }
                //cell.revealed = true;
                state[x, y] = cell;
            }
        }
    }

    private int CountMines(int cellX, int cellY)
    {
        int count = 0;
        for(int adjX = -1; adjX <= 1; adjX++)
        {
            for(int adjY = -1; adjY <= 1; adjY++)
            {
                if(adjX == 0 && adjY == 0)
                {
                    continue;
                }
                int x = cellX + adjX;
                int y = cellY + adjY;
                if(GetCell(x, y).type == Cell.Type.Mine)
                {
                    count++;
                }
            }
        }
        return count;
    }

    private void Update()
    {
        if (Input.GetKeyDown(KeyCode.R))
        {
            NewGame();
        }
        if (!gameover)
        {
            if (Input.GetMouseButtonDown(1))
            {
                Flag();
            }
            else if (Input.GetMouseButtonDown(0))
            {
                Reveal();
            }
        }
    }

    private void Flag()
    {
        Vector3 worldPosition = Camera.main.ScreenToWorldPoint(Input.mousePosition);
        Vector3Int cellPosition = board.tilemap.WorldToCell(worldPosition);
        Cell cell = GetCell(cellPosition.x, cellPosition.y);

        if (cell.type == Cell.Type.Invalid || cell.revealed)
        {
            return;
        }
        cell.flagged = !cell.flagged;
        state[cellPosition.x, cellPosition.y] = cell;
        board.Draw(state);
    }

    private void Reveal()
    {
        Vector3 worldPosition = Camera.main.ScreenToWorldPoint(Input.mousePosition);
        Vector3Int cellPosition = board.tilemap.WorldToCell(worldPosition);
        Cell cell = GetCell(cellPosition.x, cellPosition.y);

        if (cell.type == Cell.Type.Invalid || cell.revealed || cell.flagged)
        {
            return;
        }

        switch (cell.type)
        {
            case Cell.Type.Mine:
                Explode(cell);
                break;
            case Cell.Type.Empty:
                Flood(cell);
                break;
            default:
                cell.revealed = true;
                state[cellPosition.x, cellPosition.y] = cell;
                CheckWinCondition();
                break;
        }
        
        board.Draw(state);
    }

    private void Flood(Cell cell)
    {
        if (cell.revealed) return;
        if (cell.type == Cell.Type.Mine || cell.type == Cell.Type.Invalid) return;
        cell.revealed = true;
        state[cell.position.x, cell.position.y] = cell;
        if (cell.type == Cell.Type.Empty)
        {
            Flood(GetCell(cell.position.x - 1, cell.position.y));
            Flood(GetCell(cell.position.x + 1, cell.position.y));
            Flood(GetCell(cell.position.x, cell.position.y - 1));
            Flood(GetCell(cell.position.x, cell.position.y + 1));
            Flood(GetCell(cell.position.x - 1, cell.position.y - 1));
            Flood(GetCell(cell.position.x - 1, cell.position.y + 1));
            Flood(GetCell(cell.position.x + 1, cell.position.y - 1));
            Flood(GetCell(cell.position.x + 1, cell.position.y + 1));
        }
    }

    private void Explode(Cell cell)
    {
        gameover = true;
        Camera.main.backgroundColor = Color.red;
        winLoseText.text = "You lose!";

        cell.revealed = true;
        cell.exploded = true;
        state[cell.position.x, cell.position.y] = cell;

        for(int x = 0; x < width; x++)
        {
            for (int y = 0; y < height; y++)
            {
                cell = state[x, y];
                if(cell.type == Cell.Type.Mine)
                {
                    cell.revealed = true;
                    state[x, y] = cell;
                }
            }
        }
    }

    private void CheckWinCondition()
    {
        for(int x = 0; x < width; x++)
        {
            for(int y = 0; y < height; y++)
            {
                Cell cell = state[x, y];
                if (cell.type != Cell.Type.Mine && !cell.revealed)
                {
                    return;
                }
            }
        }
        gameover = true;
        Camera.main.backgroundColor = Color.green;
        winLoseText.text = "You win!";

        for (int x = 0; x < width; x++)
        {
            for (int y = 0; y < height; y++)
            {
                Cell cell = state[x, y];
                if (cell.type == Cell.Type.Mine)
                {
                    cell.flagged = true;
                    state[x, y] = cell;
                }
            }
        }
    }

    private Cell GetCell(int x, int y)
    {
        if (IsValid(x, y))
        {
            return state[x, y];
        } else
        {
            return new Cell();
        }
    }

    private bool IsValid(int x, int y)
    {
        return x >= 0 && x < width && y >= 0 && y < height;
    }

    private void InitTemp()
    {
        tempWidth = width;
        tempHeight = height;
        if(mineCount > width*height)
        {
            tempMines = (width*height) / 2;
            Debug.Log("ERROR: Too many mines! Reduced to half play space");
        }
        else
        {
            tempMines = mineCount;
        }
    }

    private void InitFromTemp()
    {
        width = tempWidth;
        height = tempHeight;
        mineCount = tempMines;
    }

    private void InitSliderListeners()
    {
        widthAndHeightSlider.onValueChanged.AddListener((v) =>
        {
            widthAndHeightSliderText.text = v.ToString("0");
            tempWidth = (int)v;
            tempHeight = (int)v;
        });
        mineSlider.onValueChanged.AddListener((v) =>
        {
            mineSliderText.text = v.ToString("0");
            tempMines = (int)v;
        });
    }
}
