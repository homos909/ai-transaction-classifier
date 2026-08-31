from abc import ABC, abstractmethod
from anthropic import Anthropic 

class ClassifierProvider(ABC):
    @abstractmethod
    def classify(self, description):
        ...

class MockProvider(ClassifierProvider):
    def classify(self, description):
        if 'thu' in description.lower() or 'bán hàng' in description.lower() or 'dịch vụ' in description.lower():
            return 'Doanh thu'
        if 'mua' in description.lower() or 'trả' in description.lower() or 'chi phí' in description.lower():
            return 'Chi phí' 
        
        return'Chưa xác định'

class AnthropicProvider(ClassifierProvider):
    def __init__(self, api_key):
        self.client = Anthropic(api_key=api_key)

    def classify(self, description):
        prompt = f"Giao dịch sau thuộc Doanh thu hay Chi phí? Chỉ trả lời đúng 1 từ: {description}"
        response = self.client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=20,
            messages=[{"role": "user", "content": prompt}]
        )

        ket_qua = response.content[0].text
        return ket_qua
    

if __name__ == "__main__":
    provider = MockProvider()
    print(provider.classify("Thu tiền bán hàng cho khách A"))
    print(provider.classify("Trả lương nhân viên tháng 9"))
        
