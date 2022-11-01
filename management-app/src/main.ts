import { NestFactory } from '@nestjs/core';
import { urlencoded, json } from 'express';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  app.use(json({ limit: "50mb" }))
  app.use(urlencoded({ limit: '50mb', extended: true }));
  await app.listen(52201);
}
bootstrap();
