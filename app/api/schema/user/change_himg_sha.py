from werkzeug.datastructures import FileStorage


def req_args_valid(parser) -> (str, bool, dict):
    parser.add_argument('head_image', dest='headimage', type=FileStorage, required=True, help="head_image error",
                        location='files')

    data = parser.parse_args()
    print(data['headimage'])
    return "success", True, data
