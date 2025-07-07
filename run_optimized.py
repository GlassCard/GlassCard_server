#!/usr/bin/env python3
"""
메모리 최적화된 GlassCard 서버 실행 스크립트
512MB 제한 환경에서 실행 가능하도록 최적화
"""

import os
import sys
import gc
import psutil
import signal
from contextlib import contextmanager

# 메모리 제한 (MB) - 512MB 제한 환경 고려
MEMORY_LIMIT_MB = 450  # 450MB로 제한하여 여유 확보

def get_memory_usage():
    """현재 메모리 사용량을 MB 단위로 반환"""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024

def optimize_memory():
    """메모리 최적화 설정"""
    # PyTorch 메모리 최적화
    os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'max_split_size_mb:64'
    
    # JVM 힙 크기 제한 (konlpy용)
    os.environ['JAVA_TOOL_OPTIONS'] = '-Xmx256m -Xms128m'
    
    # Python 가비지 컬렉션 강화
    gc.set_threshold(100, 5, 5)
    
    print("🧹 메모리 최적화 설정 완료")

def check_memory_limit():
    """메모리 제한 확인"""
    current_memory = get_memory_usage()
    if current_memory > MEMORY_LIMIT_MB:
        print(f"⚠️  메모리 사용량이 제한을 초과했습니다: {current_memory:.1f}MB > {MEMORY_LIMIT_MB}MB")
        return False
    return True

@contextmanager
def memory_monitor():
    """메모리 사용량을 모니터링하는 컨텍스트 매니저"""
    print(f"🚀 GlassCard 서버를 메모리 제한 {MEMORY_LIMIT_MB}MB로 시작합니다...")
    
    def signal_handler(signum, frame):
        print("\n🛑 서버를 종료합니다...")
        gc.collect()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        yield
    except KeyboardInterrupt:
        print("\n🛑 사용자에 의해 서버가 중단되었습니다.")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
    finally:
        print("🧹 메모리를 정리합니다...")
        gc.collect()
        print(f"📊 최종 메모리 사용량: {get_memory_usage():.1f}MB")

def main():
    """메인 실행 함수"""
    with memory_monitor():
        # 초기 메모리 사용량 확인
        initial_memory = get_memory_usage()
        print(f"📊 초기 메모리 사용량: {initial_memory:.1f}MB")
        
        # 메모리 최적화
        optimize_memory()
        gc.collect()
        
        # 메모리 제한 확인
        if not check_memory_limit():
            print("❌ 메모리 부족으로 서버를 시작할 수 없습니다.")
            print("💡 해결 방법:")
            print("   1. 다른 프로그램을 종료하여 메모리 확보")
            print("   2. requirements_minimal.txt 사용")
            print("   3. HUGGINGFACE_TOKEN 환경 변수 설정")
            print("   4. 더 작은 모델 사용")
            sys.exit(1)
        
        # main.py 실행
        print("🔧 GlassCard 서버를 시작합니다...")
        os.system("python main.py")

if __name__ == "__main__":
    main() 