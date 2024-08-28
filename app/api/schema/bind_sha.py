def bind_sha(parser) -> dict:
    """
    绑定MFA参数校验
    :param parser:参数对象
    :return: 参数数据
    """
    # 校验码
    parser.add_argument('code', type=str, required=True, location="form")
    # 密钥
    parser.add_argument('secret', type=str, required=True, location="form")
    data = parser.parse_args()

    if not data['code'].strip():
        raise ValueError("校验码为空")
    if not data['secret'].strip():
        raise ValueError("秘钥为空")

    return data
