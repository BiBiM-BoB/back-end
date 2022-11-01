import { Entity, Column, PrimaryGeneratedColumn } from "typeorm";

@Entity({name: "tools"})
export class Tool {

  @PrimaryGeneratedColumn({type: 'int'})
  id: string;

  @Column('varchar', { length: 50 })
  name: string;

  @Column('varchar', { length: 20 })
  stage: string;

  @Column()
  createAt: Date;

  @Column()
  updateAt: Date;

  @Column()
  deleteAt?: Date;
}