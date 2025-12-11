# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\web\security\web_security_manager.py
# Última atualização: 2025-12-11T09:59:27.855343

class WebSecurityManager:
    """
    Gerencia políticas de segurança do MindScan Web.
    """

    @staticmethod
    def build_policy():
        return {
            "headers": {
                "X-Frame-Options": "DENY",
                "X-Content-Type-Options": "nosniff",
                "Content-Security-Policy": "default-src 'self'"
            },
            "session_timeout": 3600
        }
