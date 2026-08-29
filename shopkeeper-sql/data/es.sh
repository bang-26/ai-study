#!/usr/bin/env bash

# ==================================================================================================
#    FileName      ：  es.sh
#    CreateTime    ：  2026-08-07 14:40:46
#    Author        ：  lihuashiyu
#    Email         ：  lihuashiyu@github.com
#    Description   ：  es.sh ==> es Docker 容器管理脚本（基于 docker-compose）
# ==================================================================================================

SCRIPT_DIR=$(dirname "$(readlink -e "$0")")                # Shell 脚本目录
COMPOSE_HOME=$(cd "${SCRIPT_DIR}/../" || exit; pwd)        # docker compose 路径

COMPOSE_FILE="${COMPOSE_HOME}/compose/es.yml"              # docker-compose 文件路径
CONTAINER_NAME="elasticsearch"                             # 容器名称
ALIAS_NAME="ElasticSearch"                                 # 显示别名
LOG_FILE="${COMPOSE_HOME}/logs/es-operation.log"           # 操作日志

RUNNING=1                                                  # 运行状态
STOP=0                                                     # 停止状态


# ========================= 状态检测 ========================= #
function service_status()
{
    local status                                           # 运行状态

    # 检查容器是否存在
    if ! docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
        echo "${STOP}"
        return
    fi

    # 检查容器运行状态
    status=$(docker inspect -f '{{.State.Status}}' "${CONTAINER_NAME}" 2>/dev/null)
    if [ "${status}" == "running" ]; then
        echo "${RUNNING}"
    else
        echo "${STOP}"
    fi
}


# ========================= 服务启动 ========================= #
function service_start()
{
    local status  ret                                      # 定义变量
    status=$(service_status)                               # 运行状态

    # 判断容器是否运行
    if [ "${status}" == "${RUNNING}" ]; then
        echo "程序（${ALIAS_NAME}）正在运行 ...... "
        return
    fi

    echo "程序（${ALIAS_NAME}）正在加载 ...... "

    # 创建并启动容器（若已存在则启动）
    docker-compose -f "${COMPOSE_FILE}" up -d >> "${LOG_FILE}" 2>&1
    sleep 2

    echo "程序（${ALIAS_NAME}）启动验证 ......"
    ret=$?
    sleep 1

    status=$(service_status)
    if [ "${status}" == "${RUNNING}" ]; then
        echo "程序（${ALIAS_NAME}）启动成功 ...... "
    else
        echo "程序（${ALIAS_NAME}）启动失败，请检查日志（${LOG_FILE}）...... "
        if [ ${ret} -ne 0 ]; then
            echo "docker-compose 返回错误码：${ret}"
        fi
    fi
}


# ========================= 服务停止 ========================= #
function service_stop()
{
    local status
    status=$(service_status)

    # 判断容器是否停止
    if [ "${status}" == "${STOP}" ]; then
        echo "程序（${ALIAS_NAME}）已经停止 ...... "
        return
    fi

    echo "程序（${ALIAS_NAME}）正在停止 ......"

    docker-compose -f "${COMPOSE_FILE}" stop >> "${LOG_FILE}" 2>&1
    sleep 1

    echo "程序（${ALIAS_NAME}）停止验证 ......"
    sleep 1

    status=$(service_status)
    if [ "${status}" == "${STOP}" ]; then
        echo "程序（${ALIAS_NAME}）停止成功 ...... "
    else
        echo "程序（${ALIAS_NAME}）停止失败，尝试强制停止 ......"
        docker-compose -f "${COMPOSE_FILE}" down  >> "${LOG_FILE}" 2>&1
        echo "程序（${ALIAS_NAME}）已强制停止 ...... "
    fi
}


# ========================= 服务停止 ========================= #
function service_restart()
{
    local status
    status=$(service_status)

    # 判断容器是否停止
    if [ "${status}" == "${STOP}" ]; then
        echo "程序（${ALIAS_NAME}）已经停止 ......"
        service_start
        return
    fi

    echo "程序（${ALIAS_NAME}）正在重启 ......"

    docker-compose -f "${COMPOSE_FILE}" restart >> "${LOG_FILE}" 2>&1
    sleep 2

    echo "程序（${ALIAS_NAME}）重启验证 ......"
    sleep 1

    status=$(service_status)
    if [ "${status}" == "${RUNNING}" ]; then
        echo "程序（${ALIAS_NAME}）重启成功 ...... "
    else
        echo "程序（${ALIAS_NAME}）重启失败，请检查日志（${LOG_FILE}）...... "
    fi
}


printf "\n================================================================================\n"
start_time=$(date +%s)
case "$1" in
    s | start | -s | --start)
        service_start
    ;;

    t | stop | -t | --stop)
        service_stop
    ;;

    r | restart | -r | --restart)
        service_restart
    ;;

    a | status | -a | --status)
        status=$(service_status)
        if [ "${status}" == "${STOP}" ]; then
            echo "程序（${ALIAS_NAME}）已经停止 ...... "
        elif [ "${status}" == "${RUNNING}" ]; then
            echo "程序（${ALIAS_NAME}）正在运行 ...... "
            # 可选：显示容器详细信息
            # docker ps --filter "name=${CONTAINER_NAME}" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
        else
            echo "程序（${ALIAS_NAME}）状态未知 ...... "
        fi
    ;;

    l | logs | -l | --logs)
        # 扩展功能：查看容器日志
        docker logs --tail 50 "${CONTAINER_NAME}" 2>&1
    ;;

    *)
        echo "    用法: $0 {start|stop|restart|status|logs}"
        echo "        +----------------------------------------+"
        echo "        | start   :  启动服务                    |"
        echo "        | stop    :  停止服务                    |"
        echo "        | restart :  重启服务                    |"
        echo "        | status  :  查看状态                    |"
        echo "        | logs    :  查看最近50条容器日志        |"
        echo "        +----------------------------------------+"
    ;;
esac

end_time=$(date +%s)
if [ "$#" -eq 1 ] && { [ "$1" == "start" ] || [ "$1" == "stop" ] || [ "$1" == "restart" ]; }; then
    echo "    脚本（$(basename "$0")）执行共消耗：$(( end_time - start_time ))s ...... "
fi
printf "================================================================================\n\n"
exit 0
