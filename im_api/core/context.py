from typing import Optional, TYPE_CHECKING
from pathlib import Path

from mcdreforged.api.all import *
from im_api.config import ImAPIConfig

if TYPE_CHECKING:
    from im_api.core.entry import ImAPI

class Context:
    """全局上下文，管理插件的全局状态"""
    
    _instance: Optional['Context'] = None
    
    def __init__(self):
        self.server: Optional[ServerInterface] = None
        self.api: Optional['ImAPI'] = None
        self._initialized = False
        self.config: Optional[ImAPIConfig] = None
    
    @property
    def logger(self):
        """获取日志记录器"""
        if self.server is None:
            raise RuntimeError("Server instance not set in Context")
        return self.server.logger
    
    @classmethod
    def get_instance(cls) -> 'Context':
        if cls._instance is None:
            cls._instance = Context()
        return cls._instance
    
    def initialize(self, server: ServerInterface) -> None:
        """初始化上下文
        
        Args:
            server: MCDR 服务器接口
        """
        self.server = server
        self._initialized = True
        
    def is_initialized(self) -> bool:
        """检查上下文是否已初始化
        
        Returns:
            是否已初始化
        """
        return self._initialized
    
    def set_api(self, api: Optional['ImAPI']) -> None:
        """设置 API 实例
        
        Args:
            api: ImAPI 实例
        """
        if not self._initialized:
            raise RuntimeError("Context not initialized")
        self.api = api
        
    def get_api(self) -> Optional['ImAPI']:
        """获取 API 实例
        
        Returns:
            ImAPI 实例，如果未设置则返回 None
        """
        if not self._initialized:
            raise RuntimeError("Context not initialized")
        return self.api
    
    def reset(self) -> None:
        """重置上下文状态"""
        self.api = None
        self.server = None
        self._initialized = False
    
    @classmethod
    def reset_instance(cls) -> None:
        """重置全局实例"""
        if cls._instance is not None:
            cls._instance.reset()
            cls._instance = None
    
    def load_config(self) -> ImAPIConfig:
        """加载配置文件"""
        try:
            # 获取MCDR工作目录
            mcdr_work_dir = Path(self.server.get_mcdr_config()['working_directory']).parent
            self.config = ImAPIConfig.load(mcdr_work_dir)
            self.logger.info("Configuration loaded successfully")
        except Exception as e:
            self.logger.error(f"Failed to load configuration: {e}")
            self.config = None
        return self.config

# 导出
__all__ = ['Context'] 