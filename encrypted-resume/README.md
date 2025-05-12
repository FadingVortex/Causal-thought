## 功能概述

1. **加密敏感信息**：通过`encryption_tool.html`页面，使用自定义密码对敏感信息进行加密。
2. **展示加密简历**：通过`encrypted_resume.html`页面，输入密码解密并展示简历内容。

---

## 使用步骤

### 1. 准备敏感信息
在`encryption_tool.html`页面中，敏感信息以JSON格式存储，包括以下内容：
- 个人信息（姓名、邮箱、电话、位置、网站）
- 教育背景
- 工作经历
- 项目经验
- 技能
- 荣誉奖项

请自行编辑其中的个人信息，然后填写入合适的密码
**密码强度建议**
 - 至少16个字符
 - 包含大小写字母、数字和特殊字符
 - 避免使用常见密码
 - 不要使用个人可猜测信息

### 2. 加密敏感信息
1. 打开`encryption_tool.html`页面。
2. 在页面中输入自定义密码。（默认密码为：“your_secure_password”）
3. 点击“生成密文”按钮，生成加密后的数据。
4. 控制台会输出加密后的JSON数据，同时页面上也会显示加密结果。

### 3. 替换加密数据
1. 将生成的加密数据复制到`encrypted_resume.html`文件中。
2. 替换`const encryptedData`变量的内容为新的加密数据。

### 4. 展示加密简历
1. 打开`encrypted_resume.html`页面。
2. 输入加密时使用的密码。
3. 解密成功后，页面将展示完整的简历内容。

---

## 技术细节

- **加密算法**：AES-CBC模式，使用CryptoJS库实现。
- **密钥生成**：通过PBKDF2算法从密码生成密钥，使用固定盐值和1000次迭代。
- **数据结构**：加密数据以JSON格式存储，解密后动态填充到网页中。

---

## 文件说明

- `encryption_tool.html`：用于生成加密数据的工具页面。
- `encrypted_resume.html`：展示加密简历的页面，支持密码解密。
- `README.md`：项目说明文档。

---

## 示例

### 加密前的敏感信息
```json
{
  "name": "张三",
  "email": "zhangsan@example.com",
  "phone": "135 1234 5678",
  "location": "北京市海淀区",
  "website": "https://zhangsan.example.com",
  "education": [...],
  "experience": [...],
  "projects": [...],
  "skills": [...],
  "awards": [...]
}
```

### 加密后的数据
```json
{
  "name": "cdc23fb685efeaa754edfa218c1c6488:0MynyGaM8/RHkPV3Z0mlWw==",
  "email": "68233289e8261a8eb2312e39633196cc:13BeNqpUXvFRWlbgvSwSwSh1v6iO4aNwuNq5hvLAjHU=",
  ...
}
```

将加密后的数据替换到`encrypted_resume.html`中的`const encryptedData`变量即可。

---

## 贡献

欢迎提交问题或建议！如需帮助，请联系项目维护者。
